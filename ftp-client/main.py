import ftplib
import os

class SimpleFTPClient:
    def __init__(self, host, port=21):
        self.host = host
        self.port = port
        self.ftp = ftplib.FTP()

    def connect(self, username='anonymous', password=''):
        try:
            self.ftp.connect(self.host, self.port)
            self.ftp.login(username, password)
            print(f"Connected to {self.host} as '{username}'")
            print(self.ftp.getwelcome())

        except ftplib.all_errors as e:
            print(f"Failed to connect: {e}")

    def list_directory(self, path='.'):
        print(f"\nDirectory Listing for {path}")
        try:
            if path:
                self.ftp.cwd(path)
            self.ftp.retrlines('LIST')

        except ftplib.all_errors as e:
            print(f"Failed to list directory: {e}")

    def download_file(self, remote_filename, local_filename):
        print(f"Downloading '{remote_filename}'...")
        try:
            with open(local_filename, 'wb') as local_file:
                self.ftp.retrbinary(f'RETR {remote_filename}', print)
                self.ftp.retrbinary(f"RETR {remote_filename}", local_file.write)
            print(f"Successfully downloaded to: {local_filename}")

        except ftplib.all_errors as e:
            print(f"Failed to download file: {e}")

    def upload_file(self, local_filename, remote_filename):
        if not os.path.isfile(local_filename):
            print(f"Error: Local file does not exist: {local_filename}")
            return

        print(f"Uploading '{local_filename}'...")
        try:
            with open(local_filename, 'rb') as local_file:
                self.ftp.storbinary(f"STOR {remote_filename}", local_file)
            print(f"Successfully uploaded as: {remote_filename}")

        except ftplib.all_errors as e:
            print(f"Failed to upload file: {e}")

    def disconnect(self):
        try:
            self.ftp.quit()
            print("Disconnected safely.")

        except ftplib.all_errors:
            self.ftp.close()
            print("Connection forced closed.")

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 2121
    
    client = SimpleFTPClient(HOST, port=PORT)

    client.connect()
    
    client.list_directory()

    client.disconnect()