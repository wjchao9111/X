#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

cmd_list = [
    [['all', 'install', 'static', ], 'git pull ; sleep 5'],
    [['all', 'install', ], 'rm -rf logs static'],
    [['all', 'install', ], 'cp -rf . /opt/sms-impl'],
    [['all', 'install', ], 'cp /opt/sms-impl/start_process.py /opt/sms-impl/cmpp2d'],
    [['all', 'install', ], 'cp /opt/sms-impl/start_filter.py /opt/sms-impl/cmpp2filter'],
    [['all', 'install', ], 'cp /opt/sms-impl/start_celery.py /opt/sms-impl/cmpp2celery'],
    [['all', 'install', ], 'cp /opt/sms-impl/start_forward.py /opt/sms-impl/forward'],
    [['all', 'install', ], 'cp conf/cmpp2d /etc/init.d/cmpp2d'],
    [['all', 'install', ], 'cp conf/cmpp2filter /etc/init.d/cmpp2filter'],
    [['all', 'install', ], 'cp conf/cmpp2celery /etc/init.d/cmpp2celery'],
    [['all', 'install', ], 'cp conf/forward /etc/init.d/forward'],
    [['all', 'install', ], 'rm -rf /opt/sms-impl/install.py'],
    [['all', 'install', ], 'dos2unix /opt/sms-impl/cmpp2d'],
    [['all', 'install', ], 'dos2unix /opt/sms-impl/cmpp2filter'],
    [['all', 'install', ], 'dos2unix /opt/sms-impl/cmpp2celery'],
    [['all', 'install', ], 'dos2unix /opt/sms-impl/forward'],
    [['all', 'install', ], 'dos2unix /etc/init.d/cmpp2d'],
    [['all', 'install', ], 'dos2unix /etc/init.d/cmpp2filter'],
    [['all', 'install', ], 'dos2unix /etc/init.d/cmpp2celery'],
    [['all', 'install', ], 'dos2unix /etc/init.d/forward'],
    [['all', 'install', ], 'chmod +x /opt/sms-impl/cmpp2d'],
    [['all', 'install', ], 'chmod +x /opt/sms-impl/cmpp2filter'],
    [['all', 'install', ], 'chmod +x /opt/sms-impl/cmpp2celery'],
    [['all', 'install', ], 'chmod +x /opt/sms-impl/forward'],
    [['all', 'install', ], 'chmod +x /etc/init.d/cmpp2d'],
    [['all', 'install', ], 'chmod +x /etc/init.d/cmpp2filter'],
    [['all', 'install', ], 'chmod +x /etc/init.d/cmpp2celery'],
    [['all', 'install', ], 'chmod +x /etc/init.d/forward'],
    [['all', 'install', ], 'mkdir logs'],
    [['all', 'install', 'static', ], 'rm -rf static'],
    [['all', 'install', 'static', ], 'mkdir static'],
    [['all', 'install', 'static', ], 'cp -rf */static/* static/'],
    # [['all', 'install', 'static', ], 'cp -rf /usr/lib/python2.7/site-packages/django/contrib/admin/static/* static/'],
    [['all', 'install', 'static', ], 'cp -rf /usr/lib64/python2.7/site-packages/django/contrib/admin/static/* static/'],
    [['all', 'install', 'static', ], 'rm -rf /opt/sms-impl/static/'],
    [['all', 'install', 'static', ], 'cp -rf static/ /opt/sms-impl/'],
    [['all', ], 'service httpd stop'],
    [['all', ], '/usr/local/apache/bin/apachectl stop'],
    [['all', ], 'service cmpp2d stop'],
    [['all', ], 'service cmpp2filter stop'],
    [['all', ], 'service cmpp2celery stop'],
    [['all', ], 'service forward stop'],
    [['all', ], 'python manage.py migrate'],
    [['all', ], 'python max_id.py'],
    [['all', ], 'service forward start'],
    [['all', ], 'service cmpp2celery start'],
    [['all', ], 'service cmpp2filter start'],
    [['all', ], 'service cmpp2d start'],
    [['all', ], '/usr/local/apache/bin/apachectl start'],
    [['all', ], 'service httpd start']]


def main():
    if len(sys.argv) < 2:
        print u'可选操作：all、install、static'
        return

    option = sys.argv[1]
    for cmd in cmd_list:
        if option in cmd[0]:
            print '$', cmd[1]
            os.system(cmd[1])


if __name__ == '__main__':
    main()
