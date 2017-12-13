from raven import Client
from .settings import SENTRY_PROJECT_URL


def send_message_to_sentry(msg):
    client = Client(SENTRY_PROJECT_URL)
    client.captureMessage(msg)
