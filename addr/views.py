# -*- coding: utf-8 -*-

from django.shortcuts import render

from X.tools.middleware import JsonResponse
from X.tools.model import get_object, object_list, auto_filter
from addr.models import AddressGroup, Address, AddressFile
from addr.tasks import addr_file_process
from addr.verify import model_default, model_check, model_filter
from base.models import Dept


@object_list
@auto_filter
def addr_list(request, grp_id):
    qs = Address.objects.all()
    grp_id = int(grp_id)
    if grp_id: qs = qs.filter(group_id=grp_id)
    return qs


def addr_export(request, grp_id, export):
    grp_id = int(grp_id)
    addr_list = Address.objects.select_related("group", "group__user", "group__dept", "group__dept__root").all()
    if grp_id:
        addr_list = addr_list.filter(group_id=grp_id)
    addr_list = model_filter(request, addr_list)
    response = render(request, 'export_addr.html', {'addr_list': addr_list})
    response['Content-Disposition'] = 'attachment; filename=%s' % 'Export.xls'
    return response


def get_grp_tree(dept_list, grp_list, visited=None, root=None):
    if not visited:
        visited = []
    node_list = []
    for dept in dept_list:
        if dept.parent == root and dept not in visited:
            node = {
                'id': '',
                'text': dept.name,
                'cls': None
            }
            visited.append(dept)
            node_list.append(node)
            children = get_grp_tree(dept_list, grp_list, visited=visited, root=dept)
            children += [{
                             'id': grp.id,
                             'text': grp.name,
                             'cls': None,
                             'checked': False,
                             'leaf': True
                         } for grp in grp_list.filter(dept=dept)]

            if children:
                node['leaf'] = False
                node['children'] = children
            else:
                node['leaf'] = True
    return node_list


def grp_tree(request):
    grp_list = AddressGroup.objects.all()
    grp_list = model_filter(request, grp_list)

    dept_list = Dept.objects.all().filter(root_id=request.session.get('user').get('dept_root_id'))

    addr_grp_tree = get_grp_tree(dept_list, grp_list, [], None)

    return JsonResponse(addr_grp_tree)


def addr_file(request):
    j_addr = request.json['object']
    j_file = request.FILES['object.file']
    print dir(j_file)
    file = AddressFile(
        name=j_file.name,
        file=j_file,
        group=get_object(AddressGroup, pk=j_addr.get('group_id')),
    )

    model_default(request, file)
    model_check(request, file)

    file.save()

    addr_file_process.delay(file.id)

    return JsonResponse({'success': True, 'message': '成功！'})
