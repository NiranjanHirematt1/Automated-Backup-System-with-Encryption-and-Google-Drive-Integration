# Automated-Backup-System-with-Encryption-and-Google-Drive-Integration

This project is a Python-based GUI application that provides an automated backup system with optional encryption and decryption features. Users can securely upload files to Google Drive or decrypt files from a local folder using this application.

Features

File Selection: Browse and select files to upload or decrypt.

Encryption: Encrypt files before uploading them to Google Drive using the cryptography library.

Decryption: Decrypt encrypted files from the local folder using a user-provided key.

Google Drive Integration: Upload files to Google Drive with the Google Drive API.

Prerequisites

To use this application, ensure you have the following installed:

Python 3.6 or higher

Required Python libraries:

tkinter (for the GUI)

cryptography (for encryption and decryption)

google-auth (for Google Drive authentication)

google-auth-oauthlib (for OAuth flow)

google-api-python-client (for interacting with Google Drive)

Google Drive API credentials:

Set up a project in the Google Cloud Console.

Enable the Google Drive API.

Download the credentials.json file and place it in the project directory.

Installation

Clone the repository:

git clone https://github.com/NiranjanHirematt1/Automated-Backup-System-with-Encryption-and-Google-Drive-Integration.git
cd Automated-Backup-System-with-Encryption-and-Google-Drive-Integration

Install the required dependencies:

pip install -r requirements.txt

Create a requirements.txt file with the following contents:

google-auth
google-auth-oauthlib
google-api-python-client
cryptography

Place the credentials.json file in the same directory as the script.

Usage

Run the script:

python script_name.py

Use the GUI to:

Select files for backup or decryption.

Check the encryption option to encrypt files before uploading.

Provide a decryption key to decrypt files.

The files will be uploaded to Google Drive or decrypted in the local directory.

Application Workflow

Backup Files:

Select files to back up.

Choose whether to encrypt the files before upload.

The files are uploaded to Google Drive.

Decrypt Files:

Select encrypted files for decryption.

Provide the decryption key.

The files are decrypted and saved in the local folder.

Notes

The encryption key is generated per session and displayed during the backup process. Ensure you save the key securely.

Use the correct decryption key when decrypting files to avoid errors.

Limitations

The application only supports file encryption with the .encrypted extension.

The decryption functionality assumes encrypted files have the .encrypted extension.

Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments

Google Drive API Documentation

Cryptography Library Documentation

Example Directory Structure

project-directory/
|-- script_name.py
|-- credentials.json
|-- token.json (auto-generated after authentication)
|-- requirements.txt

References

Google Cloud Console

Python Cryptography Library

can you make this as like i can just copy and past thire 
