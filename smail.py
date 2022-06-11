import sys,os,platform,smtplib,ssl,re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders   
from getpass import getpass
from termcolor import colored


def Login():
    print(colored("[############################# LOGIN ############################]\n","yellow"))
    try:
        smtp_server = "smtp.gmail.com"
        port = 587
        while True:
            user = input(colored("[*] Gmail ","yellow"))
            if(re.fullmatch(regex,user) and user.endswith("@gmail.com")):
                break
            print(colored("[!] Invalid email!","red"))
        while True:
            password = getpass(colored("[*] Password: ","yellow"))
            if not len(password) < 8 or len(password) >= 30:
                break
            print(colored("[!] Invalid password!","red"))
        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(user, password)
            return server, user
        except Exception:
            print(colored("[!] Invalid login or password!","red"))
            server.quit()
            sys.exit()
    except KeyboardInterrupt:
        sys.exit()

def Target(server,user):
    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    print(colored("[############################# SEND TO ###########################]\n","yellow"))
    try:
        print(colored(f"[*] From: {user}","yellow"))
        while True:
            path = input(colored("[*] File path containing email addresses: ","yellow"))
            if os.path.exists(path) == True and path.endswith(".txt") == True:
                print(colored("[*] The file path containing email addresses has been selected!","yellow"))
                break
            print(colored("[!] File not found!","red"))
        while True:
            subject = input(colored("[*] Subject: ","yellow"))
            if len(subject) != 0:
                print()
                break
        while True:
            message = input(colored("[*] Message: ","yellow"))
            if len(message) != 0:
                print()
                break
        while True:
            choose = input(colored("[*] Attach file for upload? Y/N: ","yellow"))
            if choose[0].lower() == "y" or choose[0].lower() == "n":
                break
        if choose[0].lower() == "y":
            Attach(server, user, path, subject, message)
        elif choose[0].lower() == "n":
            noAttach(server,user,path,subject, message)
    except KeyboardInterrupt:
        server.quit()
        sys.exit()


def Attach(server,user,path,subject, message):
    try:
        while True:
            filepath = input(colored("[*] File path to attach: ","yellow"))
            if os.path.exists(filepath) == True:
                print(colored("[+] The file has been selected!","yellow"))
                break
            print(colored("[!] File not found!","red"))
        filename = os.path.basename(filepath)
        with open(path) as mail_list:
            for email in mail_list:
                email = email.lower()
                email = email.strip()
                if(re.fullmatch(regex,email)):
                    data = MIMEMultipart()
                    data["From"] = user
                    data["To"] = email
                    data["Subject"] = subject
                    data.attach(MIMEText(message,"plain"))
                    attachment = open(filepath,"rb")
                    anx = MIMEBase("application", "octet-stream")
                    anx.set_payload(attachment.read())
                    encoders.encode_base64(anx)
                    anx.add_header("Content-Disposition",f"attachment; filename = {filename}")
                    attachment.close()
                    data.attach(anx)
                    try:
                        print(colored("[*] Sending...","yellow"))
                        server.sendmail(data["From"],data["To"],data.as_string())
                    except Exception:
                        print(colored("[!] Failed to send!","red"))
                    else:
                        print(colored(f"[+] From: {user}","blue"))
                        print(colored(f"[+] To: {email}","blue"))
                        print(colored(f"[+] Subject: {subject}","blue"))
                        print(colored(f"[+] Message: {message}","blue"))
                        print(colored(f"[+] File: {filename}","blue"))
        print(colored("\nFinished!","yellow"))
        server.quit()
        sys.exit()
    except KeyboardInterrupt:
        server.quit()
        sys.exit()


def noAttach(server,user,path,subject,message):
    try:
        with open(path) as mail_list:
            for email in mail_list:
                email = email.lower()
                email = email.strip()
                if(re.fullmatch(regex,email)):
                    data = "To:" + email + "\n" + "Subject: " + subject + "\n" + message
                    try:
                        print(colored("[*] Sending...","yellow"))
                        server.sendmail(user, email, data)
                    except Exception:
                        print(colored("[!] Failed to send!","red"))
                    else:
                        print(colored(f"[+] From: {user}","blue"))
                        print(colored(f"[+] To: {email}","blue"))
                        print(colored(f"[+] Subject: {subject}","blue"))
                        print(colored(f"[+] Message: {message}","blue"))                
        print(colored("\nFinished!","yellow"))
        server.quit()
        sys.exit()
    except KeyboardInterrupt:
        server.quit()
        sys.exit()
regex = r'\b[A-Za-z0-9_.-]+@[A-Za-z.]+\.[A-Z|a-z]{2,}\b'
if __name__ == "__main__":
    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    print(colored("""

                                            ███████╗███╗   ███╗ █████╗ ██╗██╗
                                            ██╔════╝████╗ ████║██╔══██╗██║██║
                                            ███████╗██╔████╔██║███████║██║██║
                                            ╚════██║██║╚██╔╝██║██╔══██║██║██║
                                            ███████║██║ ╚═╝ ██║██║  ██║██║███████╗
                                            ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
    ""","yellow"))
    print(colored("Type Ctrl+C to exit.\n\n","yellow"))
    server,user = Login()
    Target(server,user)
