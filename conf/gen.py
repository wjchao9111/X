import os
import datetime

ifcfg_file = '/etc/sysconfig/network-scripts/ifcfg-enp4s0f1'
base_ip = '111.11.84'
all_ip = [[41, 139], [141, 250], ]
prefix = 24

ifcfg_template = '''IPADDR%s=%s.%s\nPREFIX%s=%s\n'''
ip_list = []
for ip_cfg in all_ip:
    ip_list += range(ip_cfg[0], ip_cfg[1] + 1)

i = 1
ifcfg_list = []
for ip in ip_list:
    ifcfg = ifcfg_template % (i, base_ip, ip, i, prefix)
    ifcfg_list.append(ifcfg)
    i += 1

f = open(ifcfg_file, 'r')
head_lines = []
tail_lines = []
find_mode = 'head'
for line in f.readlines():
    if find_mode == 'head':
        if line.startswith('IPADDR1='):
            find_mode = 'tail'
        else:
            head_lines.append(line)
    elif find_mode == 'tail':
        if line.startswith('IPADDR='):
            find_mode = 'end'
            tail_lines.append(line)
    elif find_mode == 'end':
        tail_lines.append(line)

ifcfg_str = ''
for line in head_lines:
    ifcfg_str += line
for line in ifcfg_list:
    ifcfg_str += line
for line in tail_lines:
    ifcfg_str += line

back_cmd = 'cp %s %s.%s' % (ifcfg_file, ifcfg_file, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
print back_cmd
os.system(back_cmd)

f = open(ifcfg_file, 'w')
f.write(ifcfg_str)
f.close()
print ifcfg_str
