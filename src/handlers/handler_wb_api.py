from db.db import getData
import time


""" Модуль для обработки json с отзывами полученными с WB """


class hanlderJson(getData):
    def __init__(self):
        super().__init__()
        self.tmp_filters = self.get_filters()
        self.filters = {
            'id': [filter_id[0] for filter_id in self.tmp_filters],
            'score_1_3': [score[1] for score in self.tmp_filters],
            'score_4_5': [score[2] for score in self.tmp_filters],
            'no_text': [txt[3] for txt in self.tmp_filters],
            'article': [artc[4] for artc in self.tmp_filters],
            'template_id': [template[5] for template in self.tmp_filters]
        }
        self.stop_word = [word[0] for word in self.get_stop_word()]
        self.templates = {'id': [i[0] for i in self.get_templates()],
                          'template': [i[1] for i in self.get_templates()]}


    def feedbaack_handler(self, feedback):
        feedback_init = {'id': feedback['id'], 'nmId': feedback['nmId']}
        if feedback['text']:
            for i in self.stop_word:
                if i in feedback['text']:
                    raise Exception('StopWordException')

            if feedback['productValuation'] == 4 or feedback['productValuation'] == 5:
                feedback_init['score_4_5'] = True
                feedback_init['score_1_3'] = False
            elif feedback['productValuation'] == 1 or feedback['productValuation'] == 2 or feedback['productValuation'] == 3:
                feedback_init['score_1_3'] = True
                feedback_init['score_4_5'] = False

            if feedback_init['nmId'] in self.filters['article']:
                start = 0
                if self.filters['article'].count(feedback_init['nmId']) > 1:
                    while True:
                        idx = self.filters['article'].index(feedback_init['nmId'], start)
                        if feedback_init['score_4_5'] and self.filters['score_4_5'][idx] and not self.filters['no_text'][idx]:
                            return {'id': feedback_init['id'], "template": self.templates['template'][self.templates['id'].index(self.filters['template_id'][idx])]}
                        elif feedback_init['score_1_3'] and self.filters['score_1_3'][idx] and not self.filters['no_text'][idx]:
                            return {'id': feedback_init['id'], "template": self.templates['template'][self.templates['id'].index(self.filters['template_id'][idx])]}
                        else:
                            start += 1
                else:
                    idx = self.filters['article'].index(feedback_init['nmId'], start)
                    if feedback_init['score_4_5'] and self.filters['score_4_5'][idx] and not self.filters['no_text'][idx]:
                        return {'id': feedback_init['id'], "template": self.templates['template'][self.templates['id'].index(self.filters['template_id'][idx])]}
                    elif feedback_init['score_1_3'] and self.filters['score_1_3'][idx] and not self.filters['no_text'][idx]:
                        return {'id': feedback_init['id'], "template": self.templates['template'][self.templates['id'].index(self.filters['template_id'][idx])]}

            else:
                for i in range(len(self.filters['id'])):
                    if feedback_init['score_4_5'] and self.filters['score_4_5'][i] and not self.filters['article'][i] and not self.filters['no_text'][i]:
                        return {'id': feedback_init['id'], 'template_text': self.templates['template'][self.templates['id'].index(self.filters['template_id'][i])]}
                    elif feedback_init['score_1_3'] and self.filters['score_1_3'][i] and not self.filters['article'][i] and not self.filters['no_text'][i]:
                        return {'id': feedback_init['id'], 'template_text': self.templates['template'][self.templates['id'].index(self.filters['template_id'][i])]}
        else:
            if feedback['productValuation'] == 4 or feedback['productValuation'] == 5:
                print(feedback['productValuation'])
                for f in range(len(self.filters['no_text'])):
                    if self.filters["no_text"][f] and self.filters["score_4_5"][f]:
                        return {'id': feedback_init['id'],'template_text': self.templates['template'][self.templates['id'].index(self.filters['template_id'][f])]}

            elif feedback['productValuation'] == 1 or feedback['productValuation'] == 2 or feedback['productValuation'] == 3:
                for f in range(len(self.filters['no_text'])):
                    if self.filters["no_text"][f] and self.filters["score_1_3"][f]:
                        return {'id': feedback_init['id'],'template_text':self.templates['template'][self.templates['id'].index(self.filters['template_id'][f])]}
