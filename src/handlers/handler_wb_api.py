from db.db import getData



""" Модуль для обработки json с отзывами полученными с WB """


class hanlderJson(getData):
    def __init__(self):
        super().__init__()
        self.tmp_filters = self.get_filter_article_stop_word()
        self.filters = {
            'id': [filter_id[0] for filter_id in self.tmp_filters],
            'article': [artc[1] for artc in self.tmp_filters],
            'stop_word': [stpwrd[2] for stpwrd in self.tmp_filters]
        }

    def feedbaack_handler(self, feedback):
        feedback_init = {'id': feedback['id'], 'nmId': feedback['nmId'], 'text': feedback['text']}

        if feedback['productValuation'] == 4 or feedback['productValuation'] == 5:
            feedback_init['score_4_5'] = True
            feedback_init['score_1_3'] = False
        elif feedback['productValuation'] == 1 or feedback['productValuation'] == 2 or feedback['productValuation'] == 3:
            feedback_init['score_1_3'] = True
            feedback_init['score_4_5'] = False

        if feedback_init['text']:
            feedback_init['no_text'] = False
            feedback_split = feedback_init['text'].split()
            for n, i in enumerate(feedback_split):
                try:
                    if i.lower() == 'не' or i.lower() == 'ни':
                        feedback_split[n] = f'{i} {feedback_split[n + 1]}'
                        feedback_split[n + 1].pop()
                except IndexError:
                    break

            if feedback_init['nmId'] in self.filters['article']:

                if self.filters['article'].count(feedback_init['nmId']) > 1:
                    start = 0
                    while True:
                        try:
                            idx = self.filters['article'].index(feedback_init['nmId'], start)
                            feedback_split = feedback_init['text'].split()
                            for i in self.filters['stop_word'][idx].split(';'):
                                for f in feedback_split:
                                    if i == f:
                                        raise Exception('StopWordException')
                            start = idx + 1
                        except ValueError:
                            break
                else:
                    idx = self.filters['article'].index(feedback_init['nmId'])
                    feedback_split = feedback_init['text'].split()
                    for i in self.filters['stop_word'][idx].split(';'):
                        for f in feedback_split:
                            if i == f:
                                raise Exception('StopWordException')

                return {'id': feedback_init['id'], 'text': self.get_filtet_template_text((feedback_init['score_1_3'], feedback_init['score_4_5'], self.filters['article'][idx], feedback_init['no_text']))}

            else:
                return {'id': feedback_init['id'], 'text': self.get_filtet_template_text((feedback_init['score_1_3'], feedback_init['score_4_5'], None, feedback_init['no_text']))}

        else:
            if feedback_init['nmId'] in self.filters['article']:
                return {'id': feedback_init['id'], 'text': self.get_filtet_template_text((feedback_init['score_1_3'], feedback_init['score_4_5'], self.filters['article'][self.filters['article'].index(feedback_init['nmId'])], feedback_init['no_text']))}

            else:
                return {'id': feedback_init['id'], 'text': self.get_filtet_template_text((feedback_init['score_1_3'], feedback_init['score_4_5'], None, feedback_init['no_text']))}