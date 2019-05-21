## goals
## 1. get slackbot working
    ## set up python virtural env
    ## in /pycon-2019, run `source .env`
## 2. feel comfortable exploring API

import json
import os
from flask import Flask
from slackeventsapi import SlackEventAdapter
import slack
from collections import defaultdict # https://stackoverflow.com/questions/9358983/dictionaries-and-default-values

# In order for our application to verify the authenticity
# of requests from Slack, we'll compare the request signature
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

# Create an instance of SlackEventAdapter, passing in our Flask server so it can bind the
# Slack specific routes. The `endpoint` param specifies where to listen for Slack event traffic.
slack_events_adapter = SlackEventAdapter(
  slack_signing_secret,
  endpoint="/slack/events"
)

# Create an instance of SlackClient for your bot to make Web API requests,
# passing your app's Bot Token.
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = slack.WebClient(token=slack_bot_token)

definitions = defaultdict(lambda: "I don't know that term!",
    apple="an apple is a red fruit",
    orange="an orange is an orange fruit",
    )

def respond_to_define(message):
        # "@slackbot define apple"
        tokens = message['text'].split(' ') #split the text based on string
        # array of string: ['@slackbot','define','apple']
        term = tokens[-1]
        definition = definitions[term]
        channel = message["channel"]
        if term in definitions.keys():
            message = "Hello <@{}>! :tada: I know the definition of that term because I am very smart. \n *{}*: {}".format(message["user"], term, definition)
        else:
            message = ":frowning: <@{}> you caught me - I don't know that term".format(message["user"])
        slack_client.chat_postMessage(channel=channel, text=message)

# When someone posts a message saying `hi` to our bot, we'll
# have the bot respond with "Hello @user! :tada:"
@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    # Get the message metadata from the `event` portion of the request.
    message = event_data["event"]

    # We're logging out the payload so you can see it's anatomy
    print(json.dumps(message, indent=4, sort_keys=True))

    # If the incoming message contains "define", then respond with a "Hello" message
    # the `subtype` check filters out messages from other bot users.
    if message.get("subtype") is None and "define" in message['text']:
        respond_to_define(message)
    elif message.get("subtype") is None and "list" in message['text']:
        # "@slackbot list"
        channel = message["channel"]
        message = "Hello <@{}>! I am very smart. I know the definition of these terms: \n - {}".format(
            message["user"],
            "\n - ".join(definitions.keys()), # joins together all subsequent keys, excluding the first key
        )
        """
         - apple
         - orange    
        """
        slack_client.chat_postMessage(channel=channel, text=message)


# Echo the user's reaction back in a thread
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    # import pdb; pdb.set_trace() # opens python debugger
    event = event_data["event"]    
    channel = event["item"]["channel"]
    thread_ts = event['item']['ts']

    # Get the reactji name from the event payload
    emoji_name = event["reaction"]

    # Reply to the message on which the reaction was added, in a thread, with the ractji as the message.
    text = ":{}:".format(emoji_name)
    slack_client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=text)


slack_events_adapter.start(port=3000, debug=True)

