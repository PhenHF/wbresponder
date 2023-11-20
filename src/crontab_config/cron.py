from crontab import CronTab


""" Класс для работы с CronTab """

class setTimeForStart:
    def __init__(self, start_time):
        self.start_time = start_time
        self.cron = CronTab(user='root')

    def create_job(self):
        job = self.cron.new(command='/home/Vladimir/wbautoresponder/venv/bin/python3 src/wb_responer.py')
        job.setall(f'0 0 {self.start_time} * *')
        self.cron.write()