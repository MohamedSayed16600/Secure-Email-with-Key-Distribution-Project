import tkinter as tk
import tkinter.font as tkFont
import smtplib
import socket
import time
from Crypto.Cipher import AES
import os, random, struct
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from EncryDecry import encrypt_file
class App:
    sender = "18P7298@eng.asu.edu.eg"
    password = "Securityproject"
    tovar=""
    userSecret=""
    recepientSecret=""
    secretKey=""
    def __init__(self, root):
        #setting title
        self.to_var=tk.StringVar()
        root.title("Secure Mail Composer")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
        (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times',size=12)
        label_To=tk.Label(root)
        label_To["font"] = ft
        label_To["fg"] = "#333333"
        label_To["justify"] = "right"
        label_To["text"] = "To:"
        label_To.place(x=40,y=40,width=70,height=25)
        label_Subject=tk.Label(root)
        label_Subject["font"] = ft
        label_Subject["fg"] = "#333333"
        label_Subject["justify"] = "right"
        label_Subject["text"] = "Subject:"
        label_Subject.place(x=40,y=90,width=70,height=25)
        self.email_To=tk.Entry(root, textvariable = self.to_var)
        self.email_To["borderwidth"] = "1px"
        self.email_To["font"] = ft
        self.email_To["fg"] = "#333333"
        self.email_To["justify"] = "left"
        self.email_To["text"] = "To"
        self.email_To.place(x=120,y=40,width=420,height=30)
        self.email_Subject=tk.Entry(root)
        self.email_Subject["borderwidth"] = "1px"
        self.email_Subject["font"] = ft
        self.email_Subject["fg"] = "#333333"
        self.email_Subject["justify"] = "left"
        self.email_Subject["text"] = "Subject"
        self.email_Subject.place(x=120,y=90,width=417,height=30)
        self.email_Body=tk.Text(root)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=50,y=140,width=500,height=302)
        button_Send=tk.Button(root)
        button_Send["bg"] = "#f0f0f0"
        button_Send["font"] = ft
        button_Send["fg"] = "#000000"
        button_Send["justify"] = "center"
        button_Send["text"] = "Send"
        button_Send.place(x=470,y=460,width=70,height=25)
        button_Send["command"] = self.button_Send_command
    def send_email(self, subject, body,attach, recipients):

        # Connect to KDS on localhost:10000 to get encrypted keys
        self.connect_to_kds(10000,self.sender,recipients)
        decryptor = AES.new(attach.encode('utf-8'), AES.MODE_ECB)
        self.secretKey=decryptor.decrypt(self.userSecret)
        print("Secret key:")
        print(self.secretKey)


        # Write the recipient's secret key to a file
        with open("wrappedkey.txt","wb") as f:
            f.write(self.recepientSecret)

        # Read the recipient's secret key from a file
        with open("wrappedkey.txt","rb") as f:
            key=f.read()


        # Write the email body to a file and encrypt it with the secret key
        with open("body.txt","wb") as f:
            f.write(body.encode("utf-8"))
        encrypt_file(self.secretKey,"body.txt","RealMessageBody.txt")
        with open("RealMessageBody.txt","rb") as f:
            file_contents = f.read()
        os.remove("body.txt")

        # Create and attach the email message
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipients
        msg.attach(MIMEText("The contents of this message are in the encrypted file RealMessageBody.txt. Use wrappedkey.txt to decrypt it.", 'plain'))
        part = MIMEApplication(file_contents)
        part['Content-Disposition'] = f'attachment; filename={os.path.basename("RealMessageBody.txt")}'
        msg.attach(part)
        part=MIMEApplication(key)
        part['Content-Disposition'] = f'attachment; filename={os.path.basename("wrappedkey.txt")}'
        part['Content-Disposition']='attachment; filename=wrappedkey.txt'
        msg.attach(part)

         # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        print("Connected")
        smtp_server.starttls()
        print("TLS OK")
        smtp_server.login(self.sender, self.password)
        print("login OK")
        smtp_server.sendmail(self.sender, recipients, msg.as_string())
        print("mail sent")
        smtp_server.quit()

    def button_Send_command(self):
        tovar=self.email_To.get()
        print(tovar)
        subject = self.email_Subject.get()
        body = self.email_Body.get("1.0","end")
        att='cd30e2acb93ba4fc97e836c8ad01c324'
        self.send_email(subject, body,att, tovar)

    def connect_to_kds(self,port,userEmail,recepientEmail):
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address
        server_address = ('localhost', port)

        key_rec=False

        try:
            
            # Connect to the server
            client_socket.connect(server_address)
            print("Connected to port", port)
            data=client_socket.recv(2048)

            # Send the Emails to the RDC
            client_socket.send(userEmail.encode('utf-8'))
            time.sleep(1)
            client_socket.send(recepientEmail.encode('utf-8'))
            counter=0

            # Receive the encrypted secret keys
            while not key_rec:
                data=client_socket.recv(2048)
                if counter==0:
                    print(data)
                    self.userSecret=data
                    counter+=1
                elif counter==1:
                    print(data)
                    self.recepientSecret=data
                    key_rec=True
            # Close the connection
            client_socket.close()
            print("Connection closed")
        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running on the specified port.")

    


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
