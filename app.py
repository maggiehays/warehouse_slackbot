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
from looker_sdk import client, models, error
import pprint

sdk = client.setup("looker.ini")
looker_api_user = sdk.me()


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


class Dictionary:
    def __init__(self):
        self.fields = []
        raw_models = sdk.all_lookml_models()
        for model in raw_models:
            for explore in model.explores:
                raw_explore = sdk.lookml_model_explore(model.name, explore.name)
                explore_name = raw_explore.name
                explore_label = raw_explore.label
                for dimension in raw_explore.fields.dimensions:
                    if dimension.description == None:
                        continue
                    else:
                        self.fields.append(
                            {
                                "field": dimension.name,
                                "field_label": dimension.label,
                                "field_short_label": dimension.label_short,
                                "field_description": dimension.description,
                                "explore": explore_name,
                                "explore_label": explore_label,
                                "type": dimension.category
                            }
                        )
    def get_description(self, token):
        explore = token.split('.')[0]
        field = token.split('.')[-1]
        description = "No Description Found"
        for f in self.fields:
            if f['explore_label'].lower() == explore.lower() and f['field_label'].lower() == field.lower():
                description = f['field_description']
                break
            else:
                continue
        return description
    def list_terms(self, explore = "all"):
        list = []
        if explore == "all":
            for f in self.fields:
                list.append(f['explore_label']+"."+f['field_label'])
        else:
            for f in self.fields:
                if f['explore_label'].lower() == explore.lower():
                    list.append(f['explore_label']+"."+f['field_label'])
        return list

definitions = Dictionary()

# definition_tokens = definitions.split('.')

# "text": "<@UNC9BFKA6> define apple",

# message = "Hello <@{}>! :tada: I know the definition of that term because I am very smart. \n *{}*: {}".format(message["user"], term, definition)
def respond_to_define(message):
        # "@slackbot define apple"
        # @slackbot 'Relationships.Killed House'
        # import pdb; pdb.set_trace() # opens python debugger
        tokens = message['text'].split('define ') #split the text based on string
        # array of string: ['@slackbot','define','apple']
        term = tokens[-1]
        channel = message["channel"]
        # _i think_ definitions.get(term) loads all of the known key values from the dictionary?
        # definition = slack_dictionary.get(term)
        definition = definitions.get_description(term) #slack_dictionary[term]['definition']
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
    event = event_data["event"]    
    channel = event["item"]["channel"]
    thread_ts = event['item']['ts']

    # Get the reactji name from the event payload
    emoji_name = event["reaction"]

    # Reply to the message on which the reaction was added, in a thread, with the ractji as the message.
    text = ":{}:".format(emoji_name)
    slack_client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=text)

@slack_events_adapter.server.route("/")
def home():
    return "Wassup I'm the waremouse"

slack_events_adapter.start(port=PORT, debug=DEBUG, host='0.0.0.0')

