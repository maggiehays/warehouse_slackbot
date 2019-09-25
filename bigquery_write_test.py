from google.cloud import bigquery
from google.oauth2 import service_account
import google.cloud.bigquery as bigquery
import datetime
import time


# TODO(developer): Set key_path to the path to the service account key
#                  file.
key_path = "/Users/maggie.hays/Desktop/lookerhack-e19d7b912c76.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)

# hard-coding values to test insert when `annotation()` is exected below
user_handle='@maggie'
term='apple'
definition='an apple is a red fruit!'
emoji='+1'

def annotation():
    # r = request.get_json() # Fetch the data action JSON
    
    # client = bigquery.Client()
    dataset_id = 'slack_emojis' # Replace with name of the BQ dataset 
    table_id = 'slack_emojis'  # replace with your table ID
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # API request

    # request variables
    # this is from Looker Data Actions example 
    # name = r['data']['name']
    # annotation = r['form_params']['annotation']
    
    # system variables
    sys_time = int(time.time()) 
    row_to_insert = [
            (
             datetime.datetime.fromtimestamp(sys_time).strftime('%Y-%m-%d %H:%M:%S'),
             user_handle, 
             term,
             definition,
             emoji             
            )
        ]
    row = client.insert_rows(table, row_to_insert)  # API request to insert row
    # return '{"looker": {"success": true,"refresh_query": true}}' # return success response to Looke

annotation()
