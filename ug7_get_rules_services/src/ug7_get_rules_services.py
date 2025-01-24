#!/usr/bin/env python3


import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("__file__"), '.')))
import xmlrpc.client
import xlwt
from xlwt import Workbook


SERVER = '192.168.84.26'
USER = 'API_Admin' 	
PASSWORD = 'Sup3rS#cretP@ssword!


server = xmlrpc.client.ServerProxy('http://' + SERVER + ':4040/rpc', verbose=False)


res = server.v2.core.login(USER, PASSWORD, {})
auth_token = res['auth_token']
fw_rules = server.v1.firewall.rules.list(auth_token, 0, 100, {})


wb = Workbook()
style_1 = xlwt.XFStyle()
style_1.alignment.wrap = 1
sheet1 = wb.add_sheet('Services')
style_2 = xlwt.easyxf('font: bold 1')
sheet1.write(0,0,'Services',style_2)
col = 1
service_names = []
for item in fw_rules['items']:
    if len(item['services']) == 1:
        for service in item['services']:
            sheet1.write(col,0,server.v1.libraries.service.fetch(auth_token, service[1])['name'],style_1)
        col += 1
    elif len(item['services']) > 1:
        service_name_arr = []
        for service in item['services']:
            service_name = server.v1.libraries.service.fetch(auth_token, service[1])['name'] + '\n'
            service_name_arr.append(service_name)
        service_name_arr[-1] = service_name_arr[-1].replace('\n', '')
        sheet1.write(col,0,service_name_arr,style_1)
        col+=1
    else:
        service_name = 'Any'
        sheet1.write(col,0,service_name,style_1)
        col+=1


file_path = os.path.join('Абсолютный', 'путь', 'до', 'создаваемого', 'файла.xls')
wb.save(file_path)


server.v2.core.logout(auth_token)
