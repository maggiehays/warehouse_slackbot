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
import yaml
from google.cloud import bigquery
from google.oauth2 import service_account
import google.cloud.bigquery as bigquery
import datetime
import time


# In order for our application to verify the authenticity
# of requests from Slack, we'll compare the request signature
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

# Create an instance of SlackEventAdapter, passing in our Flask server so it can bind the
# Slack specific routes. The `endpoint` param specifies where to listen for Slack event traffic.
slack_events_adapter = SlackEventAdapter(
  slack_signing_secret,
  endpoint="/slack/events"
)

PORT = os.environ.get('PORT', 3000)
DEBUG = os.environ.get('DEBUG', False)

# Create an instance of SlackClient for your bot to make Web API requests,
# passing your app's Bot Token.
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = slack.WebClient(token=slack_bot_token)

extract_terms = open('definitions.yaml', 'r')    # 'definitions.yaml' contains a single YAML document.

slack_dictionary = yaml.load(extract_terms)

# Google BigQuery access creditenials
key_path = "/Users/maggie.hays/Desktop/lookerhack-e19d7b912c76.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)

# print(yaml.dump(slack_dictionary))
# apple:
#   definition: an apple is a red fruit!
#   emoji: apple
# banana:
#   definition: bananas as gross, knock it off
#   emoji: person_frowning
# orange:
#   definition: an orange is an orange fruit!
#   emoji: orange

# tokens = 'define apple'.split(' ')
# term = tokens[-1]
# definition = slack_dictionary[term]['definition']
# print(definition)


# message = "Hello <@{}>! :tada: I know the definition of that term because I am very smart. \n *{}*: {}".format(message["user"], term, definition)
def respond_to_define(message):
        # "@slackbot define apple"
        tokens = message['text'].split(' ') #split the text based on string
        # array of string: ['@slackbot','define','apple']
        term = tokens[-1]
        channel = message["channel"]
        # _i think_ definitions.get(term) loads all of the known key values from the dictionary?
        # definition = slack_dictionary.get(term)
        definition = slack_dictionary[term]['definition']
        if definition:
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
            "\n - ".join(slack_dictionary.keys()), # joins together all subsequent keys, excluding the first key
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
    
    #BQ table and client credentials
    dataset_id = 'slack_emojis' # Replace with name of the BQ dataset 
    table_id = 'slack_emojis'  # replace with your BQ table ID
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # BQ API request

    # slack message and emoji details
    event = event_data["event"]    
    channel = event["item"]["channel"]
    thread_ts = event['item']['ts']
    user = event["user"]

    # Get the reactji name from the event payload
    emoji_name = event["reaction"]


    # Reply to the message on which the reaction was added, in a thread, with the ractji as the message.
    text = ":{}:".format(emoji_name)
    slack_client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=text)

    # system variables
    sys_time = int(time.time()) 
    row_to_insert = [
            (
             datetime.datetime.fromtimestamp(sys_time).strftime('%Y-%m-%d %H:%M:%S'),
             user_handle, 
             # term,
             # definition,
             emoji_name             
            )
        ]
    row = client.insert_rows(table, row_to_insert)  # API request to insert row

# # hard-coding values to test insert when `annotation()` is exected below
# user_handle='@maggie'
# term='apple'
# definition='an apple is a red fruit!'
# emoji='+1'




@slack_events_adapter.server.route("/")
def home():
    return "Wassup I'm the waremouse"

slack_events_adapter.start(port=PORT, debug=DEBUG, host='0.0.0.0')

