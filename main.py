import os
import tkinter as tk
from tkinter import filedialog
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from cryptography.fernet import Fernet

SCOPES = ["https://www.googleapis.com/auth/drive"]

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Backup System")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Label for selecting files to backup
        self.file_label = tk.Label(self.root, text="Select files to backup:")
        self.file_label.pack()
        
        # Button to select files
        self.file_button = tk.Button(self.root, text="Browse Files", command=self.browse_files)
        self.file_button.pack()
        
        # Checkbox for encryption
        self.encrypt_var = tk.IntVar()
        self.encrypt_check = tk.Checkbutton(self.root, text="Encrypt files before upload", variable=self.encrypt_var)
        self.encrypt_check.pack()
        
        # Checkbox for decryption
        self.decrypt_var = tk.IntVar()
        self.decrypt_check = tk.Checkbutton(self.root, text="Decrypt files from local folder", variable=self.decrypt_var)
        self.decrypt_check.pack()
        
        # Entry field for decryption key
        self.key_label = tk.Label(self.root, text="Decryption Key:")
        self.key_label.pack()
        self.key_entry = tk.Entry(self.root, show="*")
        self.key_entry.pack()
        
        # Button to start backup/restore
        self.action_button = tk.Button(self.root, text="Start", command=self.perform_action)
        self.action_button.pack()
        
    def browse_files(self):
        if self.decrypt_var.get():
            self.files_to_decrypt = filedialog.askopenfilenames()
        else:
            self.files_to_backup = filedialog.askopenfilenames()
        
    def perform_action(self):
        if self.encrypt_var.get():
            self.backup_files()
        elif self.decrypt_var.get():
            self.decrypt_files()
        else:
            print("Please select an action: Backup or Restore.")
        
    def backup_files(self):
        creds = self.get_credentials()
        service = build("drive", "v3", credentials=creds)
        
        for file_path in self.files_to_backup:
            if self.encrypt_var.get():
                self.encrypt_file(file_path)
                file_path += ".encrypted"
            
            file_metadata = {"name": os.path.basename(file_path)}
            media = MediaFileUpload(file_path)
            
            try:
                upload_file = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields="id"
                ).execute()
                print("Backed up file:", file_metadata['name'])
            except HttpError as e:
                print("ERROR:", str(e))
            
            if self.encrypt_var.get():
                self.root.after(1000, self.delete_encrypted_file, file_path)
                # Don't print encryption key during backup

    def decrypt_files(self):
        if not hasattr(self, 'files_to_decrypt'):
            print("No files selected for decryption.")
            return
        
        key = self.key_entry.get().encode()
        for file_path in self.files_to_decrypt:
            if file_path.endswith('.encrypted'):
                success = self.decrypt_file(file_path, key)
                if success:
                    print("Decryption successful for:", file_path)
            else:
                print("Skipping decryption for:", file_path)
    
    def delete_encrypted_file(self, file_path):
        os.remove(file_path)
    
    def get_credentials(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def encrypt_file(self, file_path):
        key = Fernet.generate_key()
        cipher = Fernet(key)
              
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = cipher.encrypt(data)
        with open(file_path + '.encrypted', 'wb') as f:
            f.write(encrypted_data)
        
        print("Encryption Key:", key.decode())
        return key
    
    def decrypt_file(self, file_path, key):
        cipher = Fernet(key)
        
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        with open(file_path[:-10], 'wb') as f:  # remove '.encrypted' from the filename
            f.write(decrypted_data)
        
        return True  # Indicate success

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
