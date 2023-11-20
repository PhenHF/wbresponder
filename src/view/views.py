from typing import Any
from db.db import getData

""" Модуль для обработки данных из базы и преобразования их в удобный для использования формат"""

""" Класс для преобразования списков кортежей из базы и возвращающий словари """
class showData(getData):
    def __init__(self):
        super().__init__()

    @property
    def show_template(self):
        template = {}
        for t in self.get_templates():
            template[t[0]] = t[1]
        return template

    @property
    def show_filter(self):
        filters = {}
        for i in self.get_filters():
            filters[i[0]] = {'score_1_3': i[1],
                             'score_4_5': i[2],
                             'no_text': i[3],
                             'article': i[4],
                             'template_id': i[5]}
        return filters


    @property
    def show_stop_word(self):
        stop_word = [i[0] for i in self.get_stop_word()]
        return stop_word


    @property
    def show_response(self):
        responses = {}
        for i in self.get_response():
            responses[i[0]] = {'feedback_id': [i[1]],
                               'response_text': [2]}
        return responses