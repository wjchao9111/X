# -*- coding: utf-8 -*-
from sms.views import send_task_prepare
from X.tools.model import keep_db_alive
from sms.models import SendTask
import os


class FileManager:
    def __init__(self, bulk_size=100):
        self.last_init_id = 0
        
    @keep_db_alive
    def fetch_new_task(self):
        task_list = SendTask.objects.filter(
            id__gt=self.last_init_id,
            stat='init'
        )
        for task in task_list:
            if task.file:
                if  os.path.exists(task.file.path):
                    send_task_prepare(task)
            if task.id > self.last_init_id:
                self.last_init_id = task.id
