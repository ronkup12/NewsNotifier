import time
import threading
from datetime import datetime, timedelta
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from YnetCrawler.YnetCrawler import YnetCrawler
from flask import Flask, request


class WhatsappBot:
    # Your Account Sid and Auth Token from twilio.com/console
    # Create your trial account for free and paste the values here:
    ACCOUNT_SID = "<ACCOUNT_SID>"
    AUTH_TOKEN = "<AUTH_TOKEN>"

    def __init__(self):
        self.bot_phone_number = 'whatsapp:+14155238886'
        self.sandbox_name = "conversation-buried"  # my Twilio sandbox
        self.client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)
        self.subscribers = {}

    def send_message(self, phone_number: str, message: str):
        if phone_number.startswith('+'):
            phone_number = f"whatsapp:{phone_number}"
        elif phone_number.startswith("whatsapp:+"):
            pass
        else:
            raise TypeError("The given phone number is not in the right format")
        sent_message = self.client.messages.create(
                            from_=self.bot_phone_number,
                            body=message,
                            to=phone_number
                          )
        return sent_message

    def get_subscribers(self):
        return set(msg.from_.replace("whatsapp:", "") for msg in self.client.messages.list()).remove(self.bot_phone_number)

    def update_subscribers(self):
        all_messages = self.client.messages.list()[::-1]
        self.subscribers = dict((msg.from_, msg.date_sent) for msg in all_messages if msg.body.lower() == f"join {self.sandbox_name}")

    def remind_about_timeout(self):
        message = f"Your subscription (of 72 hours) expires in 24 hours. " \
                  f"You can rejoin anytime by replying 'join {self.sandbox_name}'"
        for subscriber, join_time in self.subscribers.items():
            if datetime.utcnow() - join_time.replace(tzinfo=None) > timedelta(hours=72-24):
                self.send_message(subscriber, message)


class YnetNotifier(WhatsappBot):
    app = Flask(__name__)
    LOCAL_PORT = 8080
    INTERVAL = 5 * 60  # 5 minutes

    def __init__(self):
        self.ynet = YnetCrawler()
        self.last_title = ""
        self.replier = threading.Thread(target=self.app.run, kwargs={"port": self.LOCAL_PORT})
        super().__init__()

    @staticmethod
    def prettify_top_story(title, subtitle, link):
        return f"_*{title}*_\n{subtitle}\n\n{link}"

    @app.route("/bot", methods=["POST"])
    def bot():
        incoming_msg = request.values.get('Body', '').lower()
        resp = MessagingResponse()
        msg = resp.message()
        if "news" in incoming_msg:
            reply = YnetNotifier.prettify_top_story(*YnetCrawler().get_top_story())
        else:
            reply = "You'll get the news when they will be available, or on demand if you request them ;)"
        msg.body(reply)
        return str(resp)

    def run(self):
        self.replier.start()
        while True:
            self.update_subscribers()
            title, subtitle, link = self.ynet.get_top_story()
            if title != self.last_title:
                self.last_title = title
                message = self.prettify_top_story(title, subtitle, link)
                for subscriber in self.subscribers:
                    self.send_message(subscriber, message)
            self.remind_about_timeout()
            time.sleep(self.INTERVAL)
        self.replier.join()


def main():
    bot = YnetNotifier()
    bot.run()


if __name__ == "__main__":
    main()
