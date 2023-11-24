from typing import Any
from db.db import getData

""" Модуль для обработки данных из базы и преобразования их в удобный для использования формат"""

""" Класс для преобразования списков кортежей из базы и возвращающий словари """
class showData(getData):
    def __init__(self):
        super().__init__()


    @property
    def show_filter(self):
        filters = {}
        for i in self.get_filters():
            filters[i[0]] = {'score_1_3': i[2],
                             'score_4_5': i[3],
                             'no_text': i[4],
                             'article': i[5],
                             'template_text': i[1],
                             'stop_words': i[6]}
        return filters


    @property
    def show_response(self):
        responses = {}
        for i in self.get_response():
            responses[i[0]] = {'feedback_id': [i[1]],
                               'response_text': [2]}
        return responses