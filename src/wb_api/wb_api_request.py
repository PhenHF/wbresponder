import requests
import base64


""" Модуль для обращения к WB api """


""" Класс для хранения токена """
class wbApiSettings:
    def __init__(self, token):
        self.token = token


""" Класс для отправки и получения данных от WB """
class wbApiRequest(wbApiSettings):
    def __init__(self, token):
        super().__init__(token)


    def get_feedbacks(self, **kwargs):
        headers = {'Authorization': self.token}
        params = kwargs
        res = requests.get('https://feedbacks-api.wildberries.ru/api/v1/feedbacks', headers=headers, params=params)
        return {'status': res.status_code, 'data': res.json()}


    def get_feedback_by_id(self, **kwargs):
        headers = {'Authorization': self.token}
        params = kwargs
        res = requests.get('https://feedbacks-api.wildberries.ru/api/v1/feedback', headers=headers, params=params)

        return {'status': res.status_code, 'data': res.json()}

    def get_xlsx(self, **kwargs):
        headers = {'Authorization': self.token}
        params = kwargs
        res = requests.get('https://feedbacks-api.wildberries.ru/api/v1/feedbacks/report', headers=headers, params=params)
        with open('report.xlsx', mode='wb') as f:
            f.write(base64.b64decode(res.json()['data']['file']))

    def post_answer(self, **kwargs):
        headers = {'Authorization': self.token}
        params = kwargs
        res = requests.patch('https://feedbacks-api.wildberries.ru/api/v1/feedbacks', headers=headers, params=params)

        return res.status_code