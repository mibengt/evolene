__author__ = 'tinglev'

import logging
import requests
from requests import HTTPError, ConnectTimeout, RequestException
from modules.util.environment import Environment
from modules.util.data import Data

class Slack(object):

    log = logging.getLogger(__name__)

    @staticmethod
    def send_to_slack(message, icon=':no_entry:'):
        for channel in Environment.get_slack_channels():
            body = Slack.get_payload_body(channel, message, icon)
            Slack.call_slack_endpoint(body)


    @staticmethod
    def on_successful_private_push(image_name):
        message = ('*{0}:{1}* pushed to KTH:s private :whale: registry, size {2}.'
                   .format(data[Data.IMAGE_NAME], data[Data.IMAGE_VERSION], data[Data.IMAGE_SIZE]))
        Slack.send_to_slack(message, icon=':jenkins:')


    @staticmethod
    def on_successful_public_push(image_name, image_version, image_size):
        message = ('*{0}:{1}* pushed to https://hub.docker.com/r/kthse/{2}/tags/, size {3}.'
                   .format(image_name, image_version, image_name, image_size)
        Slack.send_to_slack(message, icon=':jenkins:')


    @staticmethod
    def on_warning(message):
        Slack.send_to_slack(message, icon=':warning:')

    @staticmethod
    def get_payload_body(channel, text, icon, username='Evolene'):
        body = {
            "channel": channel,
            "text": text,
            "username": username,
            "icon_emoji": icon
        }
        return body

    @staticmethod
    def call_slack_endpoint(payload):
        try:
            web_hook = Environment.get_slack_web_hook()
            response = requests.post(web_hook, json=payload)
        except HTTPError as http_ex:
            Slack.log.error('Slack endpoint threw HTTPError with response "%s"', http_ex.response)
        except ConnectTimeout as timeout:
            Slack.log.error('Timeout while trying to post to Slack endpoint: "%s"', timeout)
        except RequestException as req_ex:
            Slack.log.error('Exception when trying to post to Slack endpoint: "%s"', req_ex)
