import tkinter as tk
from tkinter import filedialog
from Crypto.Cipher import AES
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
from EncryDecry import decrypt_file


"""
Change the variable self.userKey to the user's key depending on the reciepient
18P7298@eng.asu.edu.eg: cd30e2acb93ba4fc97e836c8ad01c324,
18P6555@eng.asu.edu.eg: 000cf325452802fc12f9434ba8c93afb
"""

class FileAttachmentApp:
    def __init__(self):
        
        self.secretKey=""
        self.userKey="d310b94fbb61e35821795d1f86b2305c"
        self.window = tk.Tk()
        self.window.title("File Decryptor")

        self.attachments = []
        self.create_widgets()

        self.message = MIMEMultipart()

    def create_widgets(self):
        
        read_button = tk.Button(self.window, text="Read Message", command=self.read_message)
        read_button.pack(pady=10)

        self.output_text = tk.Text(self.window, height=10, width=40, state=tk.DISABLED)
        self.output_text.pack()

        scrollbar = tk.Scrollbar(self.window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)


    def read_message(self):
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        with open("wrappedkey.txt", 'rb') as file:
            encryptedSecretKey = file.read()
            decryptor = AES.new(self.userKey.encode('utf-8'), AES.MODE_ECB)
            print(type(encryptedSecretKey))
            self.secretKey=decryptor.decrypt(encryptedSecretKey)

        decrypt_file(self.secretKey,"RealMessageBody.txt","DecryptedMessage.txt")
        
        with open("DecryptedMessage.txt","rb") as f:
            decryptedMessage = f.read()
            self.output_text.insert(tk.END, decryptedMessage)
            self.output_text.insert(tk.END, "\n\n")
        self.output_text.config(state=tk.DISABLED)

    def run(self):
        self.window.mainloop()

app = FileAttachmentApp()
app.run()
