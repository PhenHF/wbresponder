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
        self.cur.execute('CREATE TABLE IF NOT EXISTS filters(id INTEGER PRIMARY KEY AUTOINCREMENT, template TEXT, score_1_3 BOOLEAN, score_4_5, no_text BOOLEAN, article INTEGER,  stop_word TEXT)')
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
    def add_filter(self, template, score_1_3, score_4_5, no_text, article, stop_word):
        self.cur.execute('INSERT INTO filters(template, score_1_3, score_4_5, no_text, article, stop_word) VALUES(?, ?, ?, ?, ?, ?)', (template, score_1_3, score_4_5, no_text, article, stop_word))
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


    """ Метод возвращает список кортежей из таблицы с фильтрами"""
    def get_filters(self):
        flt = self.cur.execute('SELECT * FROM filters').fetchall()
        return flt

    def get_filter_article_stop_word(self):
        flt = self.cur.execute('SELECT id, article, stop_word FROM filters').fetchall()
        return flt

    def get_filtet_template_text(self, values):
        text = self.cur.execute('SELECT template_text FROM filters WHERE score_1_3 = ? score_4_5 = ? article = ? no_text = ?', values).fetchone()[0]
        return text

    def get_response(self):
        response = self.cur.execute('SELECT * FROM repsonses').fetchall()
        return response


    def get_stop_words_article(self, article):
        stop_word = self.cur.execute('SELECT stop_word FROM filters WHERE article = ?', (article, )).fetchall()
        return stop_word



""" Класс для изменения информации в базе """
class updateData(connectDB):
    def __init__(self):
        super().__init__()


    """ Метод для изменения фильтра """
    def update_filter(self, filter_id, update_field, value):
        self.cur.execute(f'UPDATE filters SET {update_field} = ? WHERE id = ?', (value, filter_id))
        self.con.commit()
        self.con.close()



""" Класс для удаления информации из базы """
class deleteData(connectDB):
    def __init__(self):
        super().__init__()


    """ Метод для удаления фильтра """
    def delete_filter(self, filter_id):
        self.cur.execute('DELETE FROM filters WHERE id = ?', (filter_id, ))
        self.con.commit()
        self.con.close()
