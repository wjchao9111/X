#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
if __name__ == '__main__':
    os.system("celery -A X worker -l info --uid apache --gid apache --autoscale=4,2")
