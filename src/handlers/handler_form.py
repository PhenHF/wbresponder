from db.db import addData, updateData
from crontab_config.cron import setTimeForStart

""" Модуль для обработки форм отправляемы пользователем """



""" Класс для обработки форм добавления """
class addFormHandler(addData):
    def __init__(self):
        super().__init__()

    def add_form_filter(self, data_form):
        self.add_filter(**data_form)


""" Класс для обработки форм обновления данных """
class updateFormHanlder(updateData):
    def __init__(self):
        super().__init__()


    def update_id_template_in_filter(self, data_form):
        self.update_filter(**data_form)


""" Класс для обработки формы и вызова нужных обработчиков"""
class handlerForm:
    def __init__(self, data_form, filter_id = None):
        self.data_form = {**data_form}
        self.filter_id = filter_id

    def add_form_handler(self):
        if not self.data_form.get('template'):
            self.data_form['template'] = None

        if self.data_form.get('score_1_3'):
            self.data_form['score_1_3'] = True
        else:
            self.data_form['score_1_3'] = False

        if self.data_form.get('score_4_5'):
            self.data_form['score_4_5'] = True
        else:
            self.data_form['score_4_5'] = False

        if self.data_form.get('no_text'):
            self.data_form['no_text'] = True
        else:
            self.data_form['no_text'] = False

        if not self.data_form.get('article'):
            self.data_form['article'] = None

        if not self.data_form.get('stop_word'):
            self.data_form['stop_word'] = None

        del self.data_form['add_filter_template']

    def update_form_hanlder(self):
        if not self.data_form['template']:
            del self.data_form['template']

        if not self.data_form['article']:
            del self.data_form['article']

        if not self.data_form['stop_word']:
            del self.data_form['stop_word']


        del self.data_form['update_filter']

    def __call__(self):
        if self.data_form.get('add_filter_template'):
            self.add_form_handler()
            print(self.data_form)
            addform = addFormHandler()
            addform.add_form_filter(self.data_form)

        if self.data_form.get('update_filter'):
            self.update_form_hanlder()
            for k, v in self.data_form.items():
                upddata = updateData()
                upddata.update_filter(self.filter_id, k, v)
