# -*- coding: utf-8 -*-
from filter.models import Filter
from X.tools.model import object_list, auto_filter


@object_list
@auto_filter
def filter_list(request, stat='all'):
    qs = Filter.objects.all()
    if stat == 'all':
        return qs
    else:
        return qs.filter(stat=stat)
