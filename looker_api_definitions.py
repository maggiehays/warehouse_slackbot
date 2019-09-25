from looker_sdk import client, models, error
import pprint

sdk = client.setup("looker.ini")
looker_api_user = sdk.me()

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

	def get_description(self, explore, field):
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
print(definitions)



