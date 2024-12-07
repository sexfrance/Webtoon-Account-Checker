<div align="center">
 
  <h2 align="center">RecaptchaV2 - Solver</h2>
  <p align="center">
This script is an asynchronous account checker for Webtoon accounts that features proxy support, RSA encryption, and efficient batch processing. It reads accounts from a text file, validates them against Webtoon's authentication servers, and provides formatted output with truncated credentials for better readability. The script uses modern async/await patterns for optimal performance and includes comprehensive error handling to manage network issues and invalid responses.
    <br />
    <br />
    <a href="https://discord.cyberious.xyz">💬 Discord</a>
    ·
    <a href="https://github.com/sexfrance/Webtoon-Account-Checker#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Webtoon-Account-Checker/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Webtoon-Account-Checker/issues">💡 Request Feature</a>
  </p>
</div>

### ⚙️ Installation

- Requires: `Python 3.7+`
- Make a python virtual environment: `python3 -m venv venv`
- Source the environment: `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (macOS, Linux)
- Install the requirements: `pip install -r requirements.txt`

---

### 🔥 Features

- Checks Webtoon accounts really fast (Valid, Invalid and Email verification pending).
- Supports both proxy and proxyless modes.
- Logs results with different levels (success, failure, warning).
- Truncates passwords to the first 8 characters for checking.

---

### 📝 Usage

- Prepare a file named `accounts.txt` with email:password combinations, one per line.

- (Optional) Prepare a file named `proxies.txt` with proxies, one per line in user:pass@ip:port format, if you want to use proxies.

- Run the script:
  ```sh
  python main.py
  ```

```python
checker = AccountChecker(proxyless=True)  # Set to True for proxyless mode
asyncio.run(checker.start())
```

### 📹 Preview

![Preview](https://i.imgur.com/oKuWM4p.gif)

---

### ❗ Disclaimers

- I am not responsible for anything that may happen, such as API Blocking, IP ban, etc.
- This was a quick project that was made for fun and personal use if you want to see further updates, star the repo & create an "issue" [here](https://github.com/sexfrance/Webtoon-Account-Checker/issues/)

---

### 📜 ChangeLog

```diff
v0.0.1 ⋮ 12/07/2024
! Initial release
```

---

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Webtoon-Account-Checker.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Webtoon-Account-Checker.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Webtoon-Account-Checker.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
