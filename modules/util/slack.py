__author__ = 'tinglev'

import logging
import requests
from requests import HTTPError, ConnectTimeout, RequestException
from modules.util.environment import Environment

class Slack(object):

    log = logging.getLogger(__name__)

    @staticmethod
    def send_to_slack(message):
        for channel in Environment.get_slack_channels():
            body = Slack.get_payload_body(channel, message)
            Slack.call_slack_endpoint(body)

    @staticmethod
    def get_payload_body(channel, text, username='Evolene',
                         icon=':triangular_flag_on_post:'):
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
            Slack.log.debug('Calling Slack with payload "%s"', payload)
            response = requests.post(web_hook, json=payload)
            Slack.log.debug('Response was "%s"', response.text)
        except HTTPError as http_ex:
            Slack.log.error('Slack endpoint threw HTTPError with response "%s"', http_ex.response)
        except ConnectTimeout as timeout:
            Slack.log.error('Timeout while trying to post to Slack endpoint: "%s"', timeout)
        except RequestException as req_ex:
            Slack.log.error('Exception when trying to post to Slack endpoint: "%s"', req_ex)