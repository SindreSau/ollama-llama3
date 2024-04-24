import json
from llama3 import get_response

# Example data for testing
DUMMY_DATASET = {
	"Qcontinuescale7[SQ001]": {
		"question_txt": "I hvilken grad er du enig i f\u00f8lgende p\u00e5stand? Jeg vil at sykehuset skal fortsette \u00e5 bruke KI-verkt\u00f8yet  [|sv\u00e6rt liten grad|sv\u00e6rt stor grad]",
		"graph_title_txt": "",
		"graph_body_txt": "",
		"phase": "4",
		"wid": "1",
		"graph_data": {
			"0": {
				"graph_type": "scale7",
				"graph_result": {
					"0": {
						"respondents": 7,
						"category": "Radiograf",
						"5": 42.9,
						"6": 14.3,
						"7": 42.9,
						"mean": 6.0
					},
					"1": {
						"respondents": 6,
						"category": "Radiolog",
						"2": 16.7,
						"5": 50.0,
						"6": 16.7,
						"7": 16.7,
						"mean": 5.0
					}
				}
			}
		},
		"number_of_respondents": "13"
	},
	"Qrecommendscale7[SQ001]": {
		"question_txt": "I hvilken grad er du enig i f\u00f8lgende p\u00e5stand? Jeg vil anbefale andre sykehus i \u00e5 ta i bruk KI-verkt\u00f8yet  [|sv\u00e6rt liten grad|sv\u00e6rt stor grad]",
		"graph_title_txt": "",
		"graph_body_txt": "",
		"phase": "4",
		"wid": "1",
		"graph_data": {
			"0": {
				"graph_type": "scale7",
				"graph_result": {
					"0": {
						"respondents": 7,
						"category": "Radiograf",
						"5": 28.6,
						"6": 28.6,
						"7": 42.9,
						"mean": 6.1
					},
					"1": {
						"respondents": 11,
						"category": "Total",
						"3": 9.1,
						"5": 36.4,
						"6": 18.2,
						"7": 36.4,
						"mean": 5.7
					}
				}
			}
		},
		"number_of_respondents": "11"
	},

}


class QuestionType:
	SCALE7 = "scale7"


def transform_data(data: dict, question_type: QuestionType = QuestionType.SCALE7) -> dict:
	"""
	Takes the data as it is currently structured for saving in the database, but then converts into a more readable format for the llama model.
	:param question_type:
	:param data:
	:return: transformed data
	"""
	# scale7 - 1=Strongly disagree, 2=Slightly disagree, 3=Neutral, 4=Neutral, 5=Slightly agree, 6=Agree, 7=Strongly agree
	if question_type == QuestionType.SCALE7:
		question = data['question_txt']
		results = {}
		for key in data['graph_data']:
			for result in data['graph_data'][key]['graph_result']:
				respondent_count = data['graph_data'][key]['graph_result'][result]['respondents']
				profession = data['graph_data'][key]['graph_result'][result]['category']
				profession_results = {}
				for i in range(1, 8):
					if str(i) in data['graph_data'][key]['graph_result'][result]:
						if i == 1:
							profession_results["Strongly disagree"] = data['graph_data'][key]['graph_result'][result][str(i)]
						elif i == 2:
							profession_results["Slightly disagree"] = data['graph_data'][key]['graph_result'][result][str(i)]
						elif i == 3:
							profession_results["Neutral"] = data['graph_data'][key]['graph_result'][result][str(i)]
						elif i == 4:
							profession_results["Neutral"] = data['graph_data'][key]['graph_result'][result][str(i)]
						elif i == 5:
							profession_results["Slightly agree"] = data['graph_data'][key]['graph_result'][result][str(i)]
						elif i == 6:
							profession_results["Agree"] = data['graph_data'][key]['graph_result'][result][str(i)]
						elif i == 7:
							profession_results["Strongly agree"] = data['graph_data'][key]['graph_result'][result][str(i)]
				results[profession] = {
					"respondents": respondent_count,
					**profession_results
				}
		transformed_data = {
			"question": question,
			"results": results
		}
		return transformed_data


if __name__ == '__main__':
	question_and_results_from_llama = {} # {question: {title: "", description: ""}}

	for index, question in enumerate(DUMMY_DATASET):
		transformed_data = transform_data(DUMMY_DATASET[question])

		# Get response from llama model
		response = get_response(str(transformed_data))
		# print(f"Response {index + 1}:\n{response}")

		# Turn the string-dict back into a dict
		response_dict = json.loads(response)

		question_and_results_from_llama[question] = response_dict

	for question, results in question_and_results_from_llama.items():
		print(f"Question: {question}")
		print(f"Title: {results['title']}")
		print(f"Description: {results['description']}")
		print()



