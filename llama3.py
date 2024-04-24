import ollama

default_system_prompt = """
You are a data analyst.
Your job is to analyse data meant for generating a graph and in turn respond with a title and description for this graph.
The data is from a survey that was conducted to understand the opinions of different medical professionals when implementing new technologies in hospitals.
You will only respond with a title and description for the graph in a JSON format:
{"title": "Title of the graph", "description": "Description of the graph"}
"""


def get_response(message, system_prompt: str=default_system_prompt):
	response = ollama.chat(model='graph_analyzer', messages=[
		{
			'role': 'system',
			'content': system_prompt,
		},
		{
			'role': 'user',
			'content': message,
		},
	])
	return response['message']['content']


# Testing data:
data = {
	"question": "I hvilken grad er du enig i f\u00f8lgende p\u00e5stand? Jeg vil at sykehuset skal fortsette \u00e5 bruke KI-verkt\u00f8yet  [|sv\u00e6rt liten grad|sv\u00e6rt stor grad]",
	"results": {
		"Lege i spesialisering": {
			"respondents": 5,
			"Disagree": 20.0,
			"Neutral": 20.0,
			"Slightly agree": 40.0,
			"Agree": 20.0,
		},
		"Radiograf": {
			"respondents": 10,
			"Neutral": 10.0,
			"Slightly agree": 30.0,
			"Agree": 30.0,
			"Strongly agree": 30.0,
		},
		"Radiolog": {
			"respondents": 8,
			"Strongly disagree": 12.5,
			"Slightly disagree": 25.0,
			"Slightly agree": 50.0,
			"Strongly agree": 12.5,
		}
	}
}


if __name__ == '__main__':
	res = get_response(str(data))
	print(res)
