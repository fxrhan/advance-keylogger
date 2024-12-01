# Keylogger with Email Logging

This is a Python-based keylogger that logs keystrokes, saves the log data to files, and periodically sends the logs via email. The program collects information such as public IP, private IP, user profile, and active window, and stores this information along with the keystrokes in log files.

## Features

- **Keylogging**: Logs keystrokes and substitutes special keys with human-readable strings (e.g., `[ENTER]`, `[CTRL+C]`).
- **Log Files**: Saves logged data to randomly named text files in either the `Documents` or `Pictures` folder.
- **Email Sending**: Periodically sends the log files via email as attachments.
- **Error Handling**: Gracefully handles errors to prevent crashes.
- **Daemon Thread**: Uses a daemon thread for sending logs in the background while the keylogger runs.
- **Cross-Platform**: Handles file paths in a platform-independent way.

## Requirements

- Python 3.x
- Required Python libraries:
  - `pynput`: For detecting key presses.
  - `requests`: For getting the public IP address.
  - `socket`: For retrieving the local IP address.
  - `smtplib`: For sending emails.
  - `win32gui`: For interacting with Windows GUI.
  - `email`: For constructing and sending emails.
  - `config`: Custom configuration module for email credentials.

Install dependencies with the following command:

```bash
pip install pynput requests pywin32
```


## Setup
- Clone or download the repository to your local machine.
- Modify the config.py file with your email address (fromAddr), email password (fromPassword), and the email recipient address (toAddr).
- Run the script using:
- ```bash
  python keylogger.py
## Example config.py:
```
fromAddr = "your-email@example.com"
fromPassword = "your-email-password"
toAddr = "recipient-email@example.com"
```
## Some Changes to be Made
If you are using a GMAIL account (recommended), you will need to change the settings to allow "Less Secure Apps" to interact with your account. This is because Gmail considers Python as a less secure application.
To enable this setting:
- Log in to your Gmail account.
- Go to Google Account Security Settings.
- Scroll down to "Less Secure App Access" and turn it ON.
(Note: Google may ask you to switch to App Passwords if "Less Secure Apps" is unavailable.)

## Keylogging
The script logs every keypress made by the user. Special keys like Enter, Backspace, Ctrl, etc., are logged with human-readable descriptions (e.g., [ENTER], [CTRL+C]). These logs are saved periodically in randomly named text files.

## Sending Logs
The script sends the saved log files via email every 10 minutes (this interval can be adjusted in the send_logs() function). The email contains the log file as an attachment.

## Files
The log files are saved in the Documents or Pictures folder of the current user's home directory. Once the logs are sent via email, the files are deleted from the local machine.
## Notes
- The script is designed for educational purposes only. Unauthorized use of keylogging software is illegal and unethical.
- Be cautious when running or deploying this script.
- The email sending functionality requires an internet connection and correct SMTP server credentials.
- The script is designed to work on Windows systems due to the use of win32gui for retrieving the active window title.
