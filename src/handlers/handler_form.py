from db.db import addData, updateData
from crontab_config.cron import setTimeForStart

""" Модуль для обработки форм отправляемы пользователем """



""" Класс для обработки форм добавления """
class addFormHandler(addData):
    def __init__(self):
        super().__init__()


    def handler_template(self, template_data):
        self.add_template(**template_data)


    def handler_filter(self, filter_data):
        self.add_filter(**filter_data)


    def handler_stop_word(self, stop_word_data):
        self.add_stop_word(**stop_word_data)


    def handler_set_start_time(self, start_time_data):
        start = setTimeForStart(**start_time_data)
        start.create_job()


""" Класс для обработки форм обновления данных """
class updateFormHanlder(updateData):
    def __init__(self):
        super().__init__()


    def update_text_template(self, new_template_text):
        self.update_template(**new_template_text)


    def update_id_template_in_filter(self, new_template_id):
        self.update_filter(**new_template_id)


""" Класс для обработки формы и вызова нужных обработчиков"""
class handlerForm(addFormHandler):
    def __init__(self, data_form):
        self.data_form = data_form


    def __call__(self):
        #Условие для добавления шаблона
        if self.data_form.get('template'):
            addform = addFormHandler()
            addform.handler_template(self.data_form)

        #Условие для добавления фильтра
        elif self.data_form.get('score_1_3') or \
            self.data_form.get('score_4_5') or \
            self.data_form.get('no_text') or \
            self.data_form.get('article'):
                addform = addFormHandler()
                addform.handler_filter(self.data_form)

        #Условие для добавления стоп слова
        elif self.data_form.get('stop_word'):
            addform = addFormHandler()
            addform.handler_stop_word(self.data_form)

        #Условие для обновления текста шаблона
        elif self.data_form.get('template_id'):
            updateform = updateFormHanlder()
            updateform.update_text_template(self.data_form)

        #Условие для обновления id шаблона который привязан к фильтру
        elif self.data_form.get('filter_id'):
            updateform = updateFormHanlder()
            updateform.update_id_template_in_filter(self.data_form)

        #Условие для установки времени запуска автоответчика
        elif self.data_form.get('start_time'):
            addform = addFormHandler()
            addform.set_start_responder_time(self.data_form)