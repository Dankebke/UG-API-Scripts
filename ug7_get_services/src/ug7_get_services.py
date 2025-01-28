#!/usr/bin/env python3

import os
import xmlrpc.client
import xlwt
from xlwt import Workbook

SERVER = '192.168.84.26'
USER = 'API_Admin' 	
PASSWORD = 'Sup3rS#cretP@ssword!

server = xmlrpc.client.ServerProxy('http://' + SERVER + ':4040/rpc', verbose=False)

res = server.v2.core.login(USER, PASSWORD, {})
auth_token = res['auth_token']
services = server.v1.libraries.services.list(auth_token, 0, 1000, {}, [])

wb = Workbook()
style_1 = xlwt.XFStyle()
style_1.alignment.wrap = 1
sheet1 = wb.add_sheet('Services')
style_2 = xlwt.easyxf('font: bold 1')
sheet1.write(0,0,'Services',style_2)
sheet1.write(0,1,'Ports',style_2)
row = 1
service_names = []
for item in services['items']:
    col = 0
    protocol_arr = []
    sheet1.write(row,col,item['name'],style_1)
    col += 1
    for protocol in item['protocols']:
        protocol_type = protocol['proto'] + '/'
        protocol_port = protocol['port'] + '\n'
        protocol_arr.append(protocol_type + protocol_port)
    protocol_arr[-1] = protocol_arr[-1].replace('\n', '')
    sheet1.write(row,col,protocol_arr,style_1)
    row += 1

file_path = os.path.join('Абсолютный', 'путь', 'до', 'создаваемого', 'файла.xls')
wb.save(file_path)

server.v2.core.logout(auth_token)
