from datetime import datetime as dt
import time

import pandas as pd

from wb_api.wb_api_request import wbApiRequest
from db.db import getData




class handlerJsonForXlsx(getData):
    def __init__(self, filename):
        super().__init__()
        self.filters = {'stop_word':[i[0] for i in self.get_stop_words_article()],
                        'article': [i[0] for i in self.get_stop_words_article()]}
        self.filename = filename


    def handler_feedback(self, token, **kwargs):
        wb_api = wbApiRequest(token)
        wb_api.get_xlsx(**kwargs, isAnswered=True)
        df_feedbacks = pd.read_excel('report.xlsx')
        df_article_wb = df_feedbacks['Артикул WB'].to_list()
        df_id_feedback = df_feedbacks['ID отзыва'].to_list()
        df_date = df_feedbacks['Дата'].to_list()
        df_article_saler = df_feedbacks['Артикул продавца'].to_list()
        df_product_valution = df_feedbacks['Количество звезд'].to_list()
        df_brand = df_feedbacks['Бренд'].to_list()
        df_text_feedback = df_feedbacks['Текст отзыва'].to_list()
        df_name = df_feedbacks['Имя'].to_list()
        df_region = df_feedbacks['Регион'].to_list()
        df_color = df_feedbacks['Цвет'].to_list()
        df_size = df_feedbacks['Размер'].to_list()
        df_usefulness = df_feedbacks['Полезность'].to_list()
        df_usefulness_minus = df_feedbacks['Полезность (количество минусов)'].to_list()
        df_barcode = df_feedbacks['Штрихкод'].to_list()
        df_answer = df_feedbacks['Ответ'].to_list()
        df_full_lists = [df_article_wb, df_id_feedback, df_date, df_article_saler, df_brand, df_text_feedback, df_name, df_region, df_color, df_size, df_usefulness, df_usefulness_minus, df_answer, df_barcode]
        for num, pv in enumerate(df_product_valution):
            if int(pv) == 5:
                for i in df_full_lists:
                    i.pop(num)

        for num, feedback in enumerate(df_text_feedback):
            feedback_list = feedback.split('')
            for n, i in enumerate(feedback_list):
                if i.lower() == 'не' or i.lower() == 'ни':
                    try:
                        feedback_list[n] = f'{i} {feedback_list[n + 1]}'
                        feedback_list[n + 1].pop()
                    except IndexError:
                        break
            for n, i in self.filters['stop_word']:
                if i in feedback_list:
                    pass

        return self.filename