from datetime import datetime as dt
import time

import pandas as pd

from wb_api.wb_api_request import wbApiRequest
from db.db import getData




class handlerJsonForXlsx(getData):
    def __init__(self, filename):
        super().__init__()
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
        df_usefulness_plus = df_feedbacks['Полезность (количество плюсов)'].to_list()
        df_usefulness_minus = df_feedbacks['Полезность (количество минусов)'].to_list()
        df_barcode = df_feedbacks['Штрихкод'].to_list()
        df_answer = df_feedbacks['Ответ'].to_list()
        df_photo = []

        df_full_lists = [df_article_wb, df_product_valution, df_id_feedback, df_date, df_article_saler, df_brand, df_text_feedback, df_name, df_region, df_color, df_size, df_usefulness_plus, df_usefulness_minus, df_answer, df_barcode]

        del_item_by_stop_word_indexes = []
        for num, pv in enumerate(df_product_valution):
            if int(pv) == 5:
                del_item_by_stop_word_indexes.append(num)

        del_item_by_stop_word_indexes.reverse()
        for i in df_full_lists:
            for n in del_item_by_stop_word_indexes:
                i.pop(n)

        for num, feedback in enumerate(df_text_feedback):
            if isinstance(feedback, str):
                feedback_list = feedback.replace(',', ' ').replace('.', ' ').replace('!',' ').replace('?', ' ').split(' ')
                for n, i in enumerate(feedback_list):
                    if i.lower() == 'не' or i.lower() == 'ни':
                        try:
                            feedback_list[n] = f'{i} {feedback_list[n + 1]}'
                            feedback_list.pop(n + 1)
                        except IndexError:
                            break

                if self.get_stop_words_article(df_product_valution[num]):
                    stop_words = [i[0] for i in self.get_stop_words_article(df_product_valution[num])]
                    del_item_by_stop_word_indexes = []
                    for word in stop_words:
                        for f in feedback_list:
                            for w in word.split(';'):
                                if f.startwith(w.lower()):
                                    del_item_by_stop_word_indexes.append(num)

                    del_item_by_stop_word_indexes.reverse()
                    for i in df_full_lists:
                        for n in del_item_by_stop_word_indexes:
                            i.pop(n)

        for feeback_id in df_id_feedback:
            feeback_by_id = wb_api.get_feedback_by_id(id=feeback_id)
            tmp_photo = []
            if feeback_by_id['data']['data']['photoLinks']:
                for i in feeback_by_id['data']['data']['photoLinks']:
                    tmp_photo.append(i['fullSize'])
                df_photo.append('\n'.join(tmp_photo))

            else:
                df_photo.append(' ')

        pd.DataFrame({'ID отзыва': df_id_feedback,
                    'Дата': df_date,
                    'Артикул продавца': df_article_saler,
                    'Артикул WB': df_article_wb,
                    'Количество звезд': df_product_valution,
                    'Бренд': df_brand,
                    'Текст отзыва': df_text_feedback,
                    'Имя': df_name,
                    'Регион': df_region,
                    'Цвет': df_color,
                    'Размер': df_size,
                    'Полезность (количество плюсов)': df_usefulness_plus,
                    'Полезность (количество минусов)': df_usefulness_minus,
                    'Штрихкод': df_barcode,
                    'Ответ': df_answer,
                    'Ссылки на фото': df_photo}).to_excel(self.filename, index=False)

        return self.filename