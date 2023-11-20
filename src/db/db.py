import sqlite3
import time


""" Модуль для работы с базой данных """



""" Подключение к базе данных и создание курсора"""
class connectDB:
    def __init__(self):
        self.con = sqlite3.connect('src/db/database.db')
        self.cur = self.con.cursor()



""" Класс для создания таблиц """
class createTable(connectDB):
    def __init__(self):
        super().__init__()


    """ Метод проверяет наличие таблицы и если ее нет то создает ее """
    def create(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS templates(id INTEGER PRIMARY KEY AUTOINCREMENT, template TEXT)')
        self.con.commit()
        self.cur.execute('CREATE TABLE IF NOT EXISTS filters(id INTEGER PRIMARY KEY AUTOINCREMENT, score_1_3 BOOLEAN, score_4_5, no_text BOOLEAN, article INTEGER, template_id INTEGER)')
        self.con.commit()
        self.cur.execute('CREATE TABLE IF NOT EXISTS stop_words(id INTEGER PRIMARY KEY AUTOINCREMENT, stop_word TEXT)')
        self.con.commit()
        self.cur.execute('CREATE TABLE IF NOT EXISTS responses(id INTEGER PRIMARY KEY AUTOINCREMENT, feedback_id, response_text TEXT, created_up TIMESTAMP, updated_up TIMESTAMP)')
        self.con.close()

ct = createTable()
ct.create()



""" Класс для добавления в базу данных """
class addData(connectDB):
    def __init__(self):
        super().__init__()


    """ Метод для добавления шаблонов """
    def add_template(self, template):
        self.cur.execute('INSERT INTO templates(template) VALUES(?)', (template, ))
        self.con.commit()
        self.con.close()


    """ Метод для добавления фильтров """
    def add_filter(self, score_1_3 = False, score_4_5 = False, no_text = False, article = None, template_id = None):
        self.cur.execute('INSERT INTO filters(score_1_3, score_4_5, no_text, article, template_id) VALUES(?, ?, ?, ?, ?)',
                         (score_1_3, score_4_5, no_text, article, template_id))
        self.con.commit()
        self.con.close()


    """ Метод для добавления стоп слов """
    def add_stop_word(self, stop_word):
        print(stop_word)
        self.cur.execute('INSERT INTO stop_words(stop_word) VALUES (?)', (stop_word, ))
        self.con.commit()
        self.con.close()


    """ Метод для сохранения id отзыва и времени ответа/редактирования ответа на отзыв """
    def add_response(self, feedback_id, response_text):
        self.cur.execute('INSERT INTO repsonses(feedback_id, response_text, created_up, updated_up) VALUES(?, ?, ?, ?)',(feedback_id, response_text, time.time(), time.time()))
        self.con.commit()
        self.con.close()



""" Класс для получения данных из базы """
class getData(connectDB):
    def __init__(self):
        super().__init__()


    """ Метод возвращает список кортежей из таблицы с шаблонами"""
    def get_templates(self):
        tmp = self.cur.execute('SELECT * FROM templates').fetchall()
        return tmp


    """ Метод возвращает список кортежей из таблицы с фильтрами"""
    def get_filters(self):
        flt = self.cur.execute('SELECT * FROM filters').fetchall()
        return flt


    """ Метод возрващает список кортейже из таблицы с стоп словами """
    def get_stop_word(self):
        stp_wrd = self.cur.execute('SELECT stop_word FROM stop_words').fetchall()
        return stp_wrd


    def get_response(self):
        response = self.cur.execute('SELECT * FROM repsonses').fetchall()
        return response



""" Класс для изменения информации в базе """
class updateData(connectDB):
    def __init__(self):
        super().__init__()


    """ Метод для изменения текста шаблона """
    def update_template(self, template_id, new_template_text):
        self.cur.execute('UPDATE templates SET template = ? WHERE id = ?', (new_template_text, template_id))
        self.con.commit()
        self.con.close()


    """ Метод для изменения id шаблона, который привязан к фильтру """
    def update_filter(self, filter_id, new_template_id):
        self.cur.execute('UPDATE filters SET template_id = ? WHERE id = ?', (new_template_id, filter_id))
        self.con.commit()
        self.con.close()

    """ Метод для изменения текста ответа в базе на отзыв """
    def update_response(self, response_text, feedback_id):
        self.cur.execute('UPDATE repsonses SET response_text = ? updated_up = ? WHERE feedback_id = ?', (response_text, feedback_id, time.time()))
        self.con.commit()
        self.con.close()



""" Класс для удаления информации из базы """
class deleteData(connectDB):
    def __init__(self):
        super().__init__()


    """ Метод для удаления шаблона """
    def delete_template(self, template_id):
        self.cur.execute('DELETE FROM templates WHERE id = ?', (template_id, ))
        self.con.commit()
        self.con.close()


    """ Метод для удаления фильтра """
    def delete_filter(self, filter_id):
        self.cur.execute('DELETE FROM filters WHERE id = ?', (filter_id, ))
        self.con.commit()
        self.con.close()


    """ Метод для удаления стоп слова """
    def delete_stop_word(self, word_id):
        self.cur.execute('DELETE FROM stop_words WHERE id = ?', (word_id, ))
        self.con.commit()
        self.con.close()