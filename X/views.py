import re

from django.shortcuts import render
from django.db import connection

from X.tools.middleware import JsonResponse
from X.tools.model import get_object
from base.models import User, Role, Permission, Dept
from addr.models import Address, AddressGroup
from sms.models import Cmpp2Cfg, QtppCfg, SendTask, Processor, CarrierSection
from filter.models import Cmpp2Cfg as FilterCmpp2Cfg, Filter


# Create your views here.
def static(request, template):
    return render(request, template, {})


def is_unique(id, type, value):
    table, column = type.split('.')
    if re.compile(r'^[a-z_A-Z0-9]*$').findall(table) and re.compile(r'^[a-z_A-Z0-9]*$').findall(column):
        cursor = connection.cursor()
        if id:
            cursor.execute('select count(*) from ' + table + ' where ' + column + ' = %s and id != %s', [value, id])
            count = cursor.fetchone()[0]
        else:
            cursor.execute('select count(*) from ' + table + ' where ' + column + ' = %s', [value])
            count = cursor.fetchone()[0]
    else:
        count = 0
    return count == 0


choices = {
    'grp.mod': AddressGroup.mod_choices,
    'addr.sex': Address.sex_choices,
    'dept.stat': Dept.stat_choices,
    'dept.type': Dept.type_choices,
    'perm.stat': Permission.stat_choices,
    'perm.type': Permission.type_choices,
    'role.stat': Role.stat_choices,
    'role.type': Role.type_choices,
    'user.stat': User.stat_choices,
    'cmpp2.stat': Cmpp2Cfg.stat_choices,
    'send.type': SendTask.type_choices,
    'send.stat': SendTask.stat_choices,
    'cmpp2.ssl': Cmpp2Cfg.ssl_choices,
    'cmpp2.msg_fmt': Cmpp2Cfg.msg_fmt_choices,
    'qtpp.stat': QtppCfg.stat_choices,
    'section.carrier': CarrierSection.carrier_choices,
    'proc.pid': Processor.pid_choices,
    'user.priority': User.priority_choices,
    'filtercmpp2.stat': FilterCmpp2Cfg.stat_choices,
    'filter.stat': Filter.stat_choices,
}


def su(request):
    uid = request.json['object']['id']
    query = User.objects.filter(id=uid)
    if query.count() == 1:
        user = query[0]
        if user.stat == 'normal':
            dept_root = user.dept.root and user.dept.root or user.dept
            admin = get_object(dept_root.dept_user_set, role__type='admin', admin=dept_root)
            request.session['user'] = {
                'id': user.id,
                'name': user.name,
                'code': user.code,
                'type': user.role.type,
                'dept_id': user.dept.id,
                'dept_name': user.dept.name,
                'dept_path': user.dept.path,
                'dept_root_id': dept_root.id,
                'dept_root_name': dept_root.name,
                'admin_id': admin is not None and admin.id or None,
            }
    return JsonResponse({'success': True, 'message': 'Success,Please press F5!'})
