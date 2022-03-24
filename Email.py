#!/usr/bin/python3
import sys, os ,string, smtplib, ssl, re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders   
from getpass import getpass
from termcolor import colored



class Email_app:
    def Banner(self):
        os.system("clear")
        print("""
                                                     ███████╗███╗   ███╗ █████╗ ██╗██╗         ██╗ ██╗  
                                                     ██╔════╝████╗ ████║██╔══██╗██║██║         ╚██╗╚██╗ 
                                                     █████╗  ██╔████╔██║███████║██║██║          ╚██╗╚██╗
                                                     ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║          ██╔╝██╔╝
                                                     ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ██╔╝██╔╝ 
                                                     ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═╝ ╚═╝  
             """)


    def Menu(self):
        try:
            print(colored("_________________________________________","blue"))
            print(colored("                 MENU","red"))
            print(colored("_________________________________________\n","blue"))
            print(colored("[0]","red"),"To exit or Ctrl+c")
            print(colored("[1]","green"),"Send an email.")
            print(colored("[2]","blue"),"Send a message to multiple emails from a text file containing the email addresses.")
            print(colored("[3]","yellow"),"Instructions.")

            while True:
                try:
                    choose = int(input(colored("Choose please: ","yellow")))
                    if choose == 0:
                        print(colored("Bye!","blue"))
                        sys.exit()
                    elif choose == 1:
                        return choose
                    elif choose == 2:
                        return choose
                    elif choose == 3:
                        return choose
                    else:
                        continue
                except ValueError:
                    continue
        except KeyboardInterrupt:
            print(colored("\nBye!","blue"))
            sys.exit()



    def Login_parser(self):
        try:
            print(colored("_________________________________________","blue"))
            print(colored("                 LOGIN","red"))
            print(colored("_________________________________________\n","blue"))
 
            regex = r'\b[A-Za-z0-9_.-]+@[A-Za-z.]+\.[A-Z|a-z]{2,}\b'
            while True:
                user = input(colored("Username: ","green"))
                if(re.fullmatch(regex, user)):
                    break
                else:
                    print(colored("Invalid email!","red"))

            while True:
                password = getpass(colored("Password: ","green"))
                if len(password) < 8 or len(password) >= 99:
                    print(colored("Invalid password!","red"))
                    continue
                else:
                    return user,password
        except KeyboardInterrupt:
            print(colored("\nBye!","blue"))
            sys.exit()


    def Login(self,user,password):
        try:

            if user.endswith("@gmail.com"):
                smtp_server = "smtp.gmail.com"
                port = 587

            elif user.endswith("@outlook.com"):
                smtp_server = "smtp.outlook.com"
                port = 587

            else:
                print(colored("Sorry, only 'gmail' and 'outlook' accounts are supported for login.","red"))
                print(colored("Bye!","blue"))
                sys.exit()

            try:
                context = ssl.create_default_context()
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()
                server.starttls(context=context)
                server.ehlo() 
                server.login(user, password)
                print(colored(f"[+] Login successfully: {user}","yellow"))
                return server, user
            except Exception:
                print(colored("Invalid login or password!","red"))
                server.quit()
                sys.exit()
        except KeyboardInterrupt:
            print("Bye!")
            server.quit()
            sys.exit()


    def Target(self,server,user):
        try:
            print(colored("_________________________________________","blue"))
            print(colored("                 SEND EMAIL","red"))
            print(colored("_________________________________________\n","blue"))
 
            regex = r'\b[A-Za-z0-9_.-]+@[A-Za-z.]+\.[A-Z|a-z]{2,}\b'
            while True:
                email = input(colored("Enter destination email: ","green"))
                if(re.fullmatch(regex, email)):
                    print()
                    break
                else:
                    print(colored("Invalid email!","red"))

            while True:
                subject = input(colored("Enter the subject: ","green"))
                if len(subject) != 0:
                    print()
                    break

            while True:
                message = input(colored("Type the message: ","green"))
                if len(message) != 0:
                    print()
                    break


            while True:
                choose = input(colored("Insert attachment Y/N? ","yellow"))
                if len(choose) == 0:
                    continue

                elif choose[0].lower()  == "y":
                    while True:
                        filename = input(colored("Enter the file name with the extension: ","green"))
                        if len(filename) == 0:
                            continue
                        elif not filename[:-3].endswith("."):
                            continue
                        else:
                            break

                    while True:
                        filepath = input(colored("Enter the file path to attach: ","green"))
                        if os.path.exists(filepath) == True:
                            print(colored(f"The {filename} file has been selected!","yellow"))
                            break
                        else:
                            print(colored("File not found!","red"))


                    data = MIMEMultipart()
                    data["From"] = user
                    data["To"] = email.strip()
                    data["Subject"] = subject
                    data.attach(MIMEText(message,"plain"))
                    try:
                        attachment = open(filepath,"rb")
                    except Exception:
                        print(colored("Failed to open file.","red"))
                        print(colored("Bye!","red"))
                        server.quit()
                        sys.exit()

                    anx = MIMEBase("application", "octet-stream")
                    anx.set_payload(attachment.read())
                    encoders.encode_base64(anx)
                    anx.add_header("Content-Disposition",f"attachment; filename = {filename}")
                    attachment.close()
                    data.attach(anx)
                    try:
                        print(colored("Sending...","yellow"))
                        server.sendmail(data["From"],data["To"],data.as_string())
                    except Exception:
                        print(colored("Failed to send!","red"))
                        print(colord("Bye!","blue"))
                        server.quit()
                        sys.exit()

                    else:
                        print(colored("_________________________________________","blue"))
                        print(colored("                 DATA SENT","red"))
                        print(colored("_________________________________________\n","blue"))

                        print(colored(f"[+] From: {user}","blue"))
                        print(colored(f"[+] To: {email}","blue"))
                        print(colored(f"[+] Subject: {subject}","blue"))
                        print(colored(f"[+] Message: {message}","blue"))
                        print(colored(f"[+] File: {filename}","blue"))
                        print(colored("\nFinished!","yellow"))
                        print(colored("Bye!","blue"))
                        server.quit()
                        sys.exit()


                elif choose[0].lower() == 'n':
                    data = "To:" + email.strip() + "\n" + "Subject: " + subject + "\n" + message
                    try:
                        print(colored("Sending...","yellow"))
                        server.sendmail(user, email, data)
                    except Exception:
                        print(colored("Failed to send!","red"))
                        print(colored("Bye!","blue"))
                        server.quit()
                        sys.exit()

                    else:
                        print(colored("_________________________________________","blue"))
                        print(colored("                 DATA SENT","red"))
                        print(colored("_________________________________________\n","blue"))
                        print(colored(f"[+] From: {user}","blue"))
                        print(colored(f"[+] To: {email}","blue"))
                        print(colored(f"[+] Subject: {subject}","blue"))
                        print(colored(f"[+] Message: {message}","blue"))
                        print(colored("\nFinished!","yellow"))
                        print(colored("Bye!","blue"))
                        server.quit()
                        sys.exit()
                else:
                    continue

        except KeyboardInterrupt:
            print(colored("\nBye!","blue"))
            server.quit()
            sys.exit()



    def Targets(self,server,user):
        try:
            print(colored("________________________________________","blue"))
            print(colored("                 SEND MULTIPLE EMAILS","red"))
            print(colored("________________________________________\n","blue"))
 
            while True:
                path = input(colored("Enter the path of the text file containing the recipient list to send the message: ","green"))
                if os.path.exists(path) == True and path.endswith(".txt") == True:
                    print(colored(f"The {path} file containing the recipient list has been selected!","yellow"))
                    break
                else:
                    print(colored("File not found!","red"))

            while True:
                subject = input(colored("Enter the subject: ","green"))
                if len(subject) != 0:
                    print()
                    break

            while True:
                message = input(colored("Type the message: ","green"))
                if len(message) != 0:
                    print()
                    break

            while True:
                choose = input(colored("Insert attachment Y/N? ","yellow"))
                if len(choose) == 0:
                    continue

                elif choose[0].lower()  == "y":
                    while True:
                        filename = input(colored("Enter the file name with the extension: ","green"))
                        if len(filename) == 0:
                            continue
                        elif not filename[:-3].endswith("."):
                            continue
                        else:
                            break

                    while True:
                        filepath = input(colored("Enter the file path to attach: ","green"))
                        if os.path.exists(filepath) == True:
                            print(colored(f"The {filename} file has been selected!","yellow"))
                            break
                        else:
                            print(colored("File not found!","red"))

                    with open(path) as mail_list:
                        regex = r'\b[A-Za-z0-9_.-]+@[A-Za-z.]+\.[A-Z|a-z]{2,}\b'
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
                                    print(colored("Sending...","yellow"))
                                    server.sendmail(data["From"],data["To"],data.as_string())
                                except Exception:
                                    print(colored("Failed to send!","red"))

                                else:
                                    print(colored("________________________________________","blue"))
                                    print(colored("                 DATA SENT","red"))
                                    print(colored("________________________________________\n","blue"))

                                    print(colored(f"[+] From: {user}","blue"))
                                    print(colored(f"[+] To: {email}","blue"))
                                    print(colored(f"[+] Subject: {subject}","blue"))
                                    print(colored(f"[+] Message: {message}","blue"))
                                    print(colored(f"[+] File: {filename}","blue"))
                            else:
                                continue
                    print(colored("\nFinished!","yellow"))
                    print(colored("Bye!","blue"))
                    server.quit()
                    sys.exit()


                elif choose[0].lower() == 'n':
                    regex = r'\b[A-Za-z0-9_.-]+@[A-Za-z.]+\.[A-Z|a-z]{2,}\b'
                    with open(path) as mail_list:
                        for email in mail_list:
                            email = email.lower()
                            email = email.strip()
                            if(re.fullmatch(regex,email)):
                                data = "To:" + email + "\n" + "Subject: " + subject + "\n" + message
                                try:
                                    print(colored("Sending...","yellow"))
                                    server.sendmail(user, email, data)
                                except Exception:
                                    print(colored("Failed to send!","red"))
                                else:
                                    print(colored("________________________________________","blue"))
                                    print(colored("                 DATA SENT","red"))
                                    print(colored("________________________________________\n","blue"))
                                    print(colored(f"[+] From: {user}","blue"))
                                    print(colored(f"[+] To: {email}","blue"))
                                    print(colored(f"[+] Subject: {subject}","blue"))
                                    print(colored(f"[+] Message: {message}","blue"))
                            else:
                                continue
                    print(colored("\nFinished!","yellow"))
                    print(colored("Bye!","blue"))
                    server.quit()
                    sys.exit()
                else:
                    continue

        except KeyboardInterrupt:
            print(colored("\nBye","blue"))
            server.quit()
            sys.exit()


    def About(self):
        print(colored("________________________________________","blue"))
        print(colored("                 INSTRUCTIONS","red"))
        print(colored("________________________________________\n","blue"))
             
        print("# Configure your Gmail account to login using this app, go to: https://myaccount.google.com/lesssecureapps")
        print("# No configuration is required to log into your Outlook account to use this app.")
        print("# You can send an email with or without files attached.")
        print("# You can send email to multiple destinations at once.")
        sys.exit()


if __name__ == "__main__":
    def main():
        app = Email_app()
        app.Banner()
        choose = app.Menu()
        if choose == 1:
            user,password = app.Login_parser()
            server,user = app.Login(user,password)
            app.Target(server,user)
        elif choose == 2:
            user,password = app.Login_parser()
            server,user = app.Login(user,password)
            app.Targets(server,user)

        elif choose == 3:
            app.About()
    main()
