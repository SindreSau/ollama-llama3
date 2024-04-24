import ollama
from huggingface_hub import hf_hub_download

# Check if the model already exists
models = ollama.list()

# Check if "graph_translator" is in the list of models
if any(model for model in models['models'] if model['name'] == 'ai_translator:latest'):
	print("Model already exists")
else:
	print("Model does not exist, downloading ...")
	# Model ID of the model to download
	model_id = "normistral-7b-warm.Q4_K_M.gguf"

	# Download the model from the Hub
	repo_id = "norallm/normistral-7b-warm"
	output_dir = "./models"
	hf_hub_download(repo_id=repo_id, filename=model_id, cache_dir=output_dir)


	# Create a ollama-model from the downloaded model
	modelfile = """FROM models/models--norallm--normistral-7b-warm/snapshots/fdb8ae6c5938effb12e13640a3914344cdc89077
	/normistral-7b-warm.Q4_K_M.gguf"""

	# Create the model, which in turn will be stored with the other ollama-models
	print("Creating model ...")
	ollama.create(model="ai_translator", modelfile=modelfile)


# Define the system prompt
def get_translation(text: str) -> str:
	text_length = len(text)
	prompt = f"Engelsk: {text}Bokmål:"
	response = ollama.chat(model='ai_translator', messages=[
		{
			'role': 'user',
			'content': prompt,
		},
	], options={'num_predict': text_length * 0.5})
	# Only return the first *text_length* characters
	return response['message']['content']


if __name__ == '__main__':
	# Define the text to be translated
	text = "In which degree do you agree with the following statement? I want the hospital to continue using the AI tool  [|very little degree|very large degree]"
	print("translating text ...")

	# Get the translation
	translation = get_translation(text)
	print(translation)

