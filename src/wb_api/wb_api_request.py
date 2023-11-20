import requests

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


    def get_archive_feedbask(self, **kwargs):
        headers = {'Authorization': self.token}
        params = kwargs
        res = requests.get('https://feedbacks-api.wildberries.ru/api/v1/feedbacks/archive', headers=headers, params=params)
        return {'status': res.status_code, 'data': res.json()}


    def post_answer(self, **kwargs):
        headers = {'Authorization': self.token}
        params = kwargs
        res = requests.patch('https://feedbacks-api.wildberries.ru/api/v1/feedbacks', headers=headers, params=params)

        return res.status_code