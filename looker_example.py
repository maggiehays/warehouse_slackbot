from looker_sdk import client, models, error

sdk = client.setup("looker.ini")
looker_api_user = sdk.me()

models = sdk.all_lookml_models()

print(models)