from datetime import datetime as dt

import pandas as pd

from wb_api.wb_api_request import wbApiRequest
from db.db import getData




class handlerJsonForXlsx(getData):
    def __init__(self, filename):
        super().__init__()
        self.stop_word = [i[0] for i in self.get_stop_word()]
        self.filename = filename


    def handler_feedback(self, tokens, **kwargs):
        df_name = []
        df_product_valuation = []
        df_article = []
        df_text = []
        df_photo = []
        for t in tokens:
            wb_api = wbApiRequest(t)
            feedbacks = wb_api.get_feedbacks(**kwargs, isAnswered=True)
            archive_feedbacks = wb_api.get_archive_feedbask(take=5000, skip=0, order='dateDesc')
            for i in feedbacks['data']['feedbacks']:
                for s in self.stop_word:
                    if s in i['text']:
                        continue
                    else:
                        if i['productValuation'] == 1 or i['productValuation'] == 2 or i['productValuation'] == 3 or i['productValuation'] == 4:
                            df_name.append(i['productDetails']['productName'])
                            df_product_valuation.append(i['productValuation'])
                            df_article.append(i['nmId'])
                            df_text.append(i['text'])
                            df_tmp_photo = []
                            for photo in i['photoLinks']:
                                df_tmp_photo.append(photo['fullSize'])

                            df_photo.append(';'.join(df_tmp_photo))
            for i in archive_feedbacks['data']['feedbacks']:
                for s in self.stop_word:
                    if s in i['text']:
                        continue
                    else:
                        if dt.strptime(kwargs['data_from'], '%d.%m.%Y') <= dt.strptime(i['createdDate'][:10], '%Y-%m-%d').timestamp() <= dt.strptime(kwargs['data_to'], '%d.%m.%Y'):
                            if i['productValuation'] == 1 or i['productValuation'] == 2 or i['productValuation'] == 3 or i['productValuation'] == 4:
                                df_name.append(i['productDetails']['productName'])
                                df_product_valuation.append(i['productValuation'])
                                df_article.append(i['nmId'])
                                df_text.append(i['text'])
                                df_tmp_photo = []
                                for photo in i['photoLinks']:
                                    df_tmp_photo.append(photo['fullSize'])

                            df_photo.append(';'.join(df_tmp_photo))

        pd.DataFrame({'Наименование': df_name,
                      'Оценка': df_product_valuation,
                      'Артикул': df_article,
                      'Текст отзыва': df_text,
                      'Ссылдка на фото': df_photo}).to_excel(self.filename, index=False)


        return self.filename