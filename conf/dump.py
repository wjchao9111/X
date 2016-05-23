import json

f = open('dump.json')
j_str = f.read()
f.close()
j_list = json.loads(j_str)

model_types = []
for j in j_list:
    if j.get('model') in model_types:
        pass
    else:
        model_types.append(j.get('model'))

dump_list = []
for j in j_list:
    if j.get('model') in [
        u'base.dept',
        u'base.permission',
        u'base.role',
        u'base.user'
    ]:
        dump_list.append(j)

dump_str = json.dumps(dump_list)

f = open('dump.json', 'w')
f.write(dump_str)
f.close()
