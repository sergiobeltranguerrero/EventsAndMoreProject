import requests


# Info de la API de SurveyMonkey (https://developer.surveymonkey.com/api/v3/)
class SurveyMonkeyAPI:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def get_survey_list(self):
        url = self.api_url + '/surveys'
        headers = {'Authorization': 'bearer ' + self.api_key, 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_survey_details(self, survey_id):
        url = self.api_url + '/surveys/' + str(survey_id) + '/details'
        headers = {'Authorization': 'Bearer ' + self.api_key}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_survey_responses(self, survey_id, page=1):
        url = self.api_url + '/surveys/' + str(survey_id) + '/responses'
        headers = {'Authorization': 'Bearer ' + self.api_key}
        params = {'page': page}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_survey_response_details(self, survey_id, response_id):
        url = self.api_url + '/surveys/' + str(survey_id) + '/responses/' + str(response_id)
        headers = {'Authorization': 'Bearer ' + self.api_key}
        response = requests.get(url, headers=headers)
        return response.json()

    def create_survey(self, title):
        url = self.api_url + '/surveys'
        headers = {'Authorization': 'Bearer ' + self.api_key, 'Content-Type': 'application/json'}
        data = {
            "title": title,
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
