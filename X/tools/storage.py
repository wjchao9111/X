# -*-coding:utf-8 -*-
import os
import random
import time
import uuid

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from X.settings import debugging, MEDIA_ROOT


class FileStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(FileStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        name = os.path.join(d, fn + ext)
        return super(FileStorage, self)._save(name, content)

    def exists(self, name):
        path = self.path(name)
        if debugging:
            path = path.encode('gbk')
        else:
            path = path.encode('utf8')
        return os.path.exists(path)


class TempFile():
    def __init__(self):
        self.path = os.path.join(MEDIA_ROOT, 'temp', str(uuid.uuid1()))
        if not os.path.exists(os.path.join(MEDIA_ROOT, 'temp')):
            os.makedirs(os.path.join(MEDIA_ROOT, 'temp'), mode=0o755)
        self.file = None

    def open(self, mode):
        if self.file:
            self.file.close()
            self.file = None
        self.file = open(self.path, mode)
        return self.file

    def write_and_save(self, data, mode='wb'):
        file = open(self.path, mode)
        file.write(data)
        file.close()

    def read_and_close(self, mode='rb'):
        file = open(self.path, mode)
        data = file.read()
        file.close()
        return data

    def close(self, remove=True):
        if self.file:
            self.file.close()
            self.file = None
        if remove:
            os.remove(self.path)
