import os
import time
from slackclient import SlackClient
import tmdb

# Futura's ID as an environment variable.
BOT_ID = os.environ.get('BOT_ID')

# constants
AT_BOT = '<@' + BOT_ID + '>'
commands = ('ssearch', 'details', 'credits')

# instantiate Slack and Twilio clients.
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


class Command:
    def __init__(self):
        pass

    def ssearch(self, command, channel):
        if command.startswith(commands):
            response = 'Sure, let me look it up!'
            slack_client.api_call('chat.postMessage', channel=channel,
                                  text=response, as_user=True)
        movies = tmdb.Search().search(command[7:])
        slack_client.api_call('chat.postMessage', channel=channel,
                              text=movies, as_user=True)

    def details(self, command, channel):
        if command.startswith(commands):
            response = 'Sure, let me look it up!'
            slack_client.api_call('chat.postMessage', channel=channel,
                                  text=response, as_user=True)
        details = tmdb.Movie(command[8:]).details()
        slack_client.api_call('chat.postMessage', channel=channel,
                              text=details, as_user=True)

    def credits(self, command, channel):
        if command.startswith(commands):
            response = 'Sure, let me look it up!'
            slack_client.api_call('chat.postMessage', channel=channel,
                                  text=response, as_user=True)
        cast, crew = tmdb.Movie(command[8:]).credits()
        slack_client.api_call('chat.postMessage', channel=channel,
                              text=crew, as_user=True)


def handle_command(command, channel):
    '''
    Receives commands directed at the bot and determines if they are valid
    commands. If so, then acts on the commands. If not, returns back what it
    needs for clarification.
    '''
    response = 'Try again! Call me and use one of these: {}.'.format(commands)
    if command.startswith(commands):
        method = getattr(Command(), command[:7])
        method(command, channel)
    else:
        slack_client.api_call('chat.postMessage', channel=channel,
                              text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    '''
    The Slack Real Time Messaging API is an events firehose. This parsing
    function returns None unless a message is directed at the Bot, based on its
    ID.
    '''
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == '__main__':
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print('Futura connected and running!')
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid Slack token or bot ID?')
