import random

from wb_api.wb_api_request import wbApiRequest
from handlers.handler_wb_api import hanlderJson
from db.db import addData
from config import get_token


class responder:
    def __init__(self, token):
        self.wbApi = wbApiRequest(token)
        self.handler = hanlderJson()

    def start_hanlder(self):
        feedbacks = self.wbApi.get_feedbacks(**{'isAnswered': False, 'take': 5000, 'skip': 0})
        add_data = addData()
        for i in feedbacks['data']['data']['feedbacks']:
            try:
                answer = self.handler.feedbaack_handler(i)
                answer['text'] = answer['text'][random.randint(0, len(answer['text'].split(';'))-1)]
                if answer:
                    self.wbApi.post_answer(**answer)
                    add_data.add_response(**answer)
            except Exception as e:
                continue





if __name__ == '__main__':
    resp = responder(get_token())
    resp.start_hanlder()