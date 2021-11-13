from environs import Env


environment = Env()
environment.read_env()

SEND_REPORT_EVERY = environment.int("SEND_REPORT_EVERY")
TELEGRAM_BOT_TOKEN = environment.str("TELEGRAM_BOT_TOKEN")
EMAIL = environment.str("EMAIL")
EMAIL_PASSWORD = environment.str("EMAIL_PASSWORD")
