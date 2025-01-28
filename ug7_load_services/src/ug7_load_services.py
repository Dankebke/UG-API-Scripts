#!/usr/bin/env python3

import os
import xmlrpc.client
import xlrd

SERVER = '192.168.84.26'
USER = 'API_Admin' 	
PASSWORD = 'Sup3rS#cretP@ssword!

server = xmlrpc.client.ServerProxy('http://' + SERVER + ':4040/rpc', verbose=False)

res = server.v2.core.login(USER, PASSWORD, {})
auth_token = res['auth_token']
dict_services = {}
all_services = server.v1.libraries.services.list(auth_token, 0, 1000, {}, [])
for item in all_services["items"]:
    dict_services.update({item["name"]:item["id"]})

file_path = os.path.join('Абсолютный', 'путь', 'до', 'файла.xls')
book = xlrd.open_workbook(file_name)
sheet1 = book.sheet_by_index(0)

for row in range(sheet1.nrows):
    if row > 0:
        protocols = []
        col = 0
        service_name = sheet1.cell_value(row, col)
        col += 1
        service_dst_ports = sheet1.cell_value(row, col).split('\n')
        service_dst_ports_stripped = [s.strip() for s in service_dst_ports]
        for service_dst_port in service_dst_ports_stripped:
            protocol = {'proto':'','port':'','source_port':''}
            service_dst_port_type = str(service_dst_port)[:service_dst_port.find('/')]
            service_dst_port_numb = str(service_dst_port)[service_dst_port.find('/')+1:]
            protocol['proto'] = service_dst_port_type
            protocol['port'] = service_dst_port_numb
            protocols.append(protocol)
        service_structure = {'name': service_name, 'description': service_desc, 'protocols': protocols}
        try:
            server.v1.libraries.service.add(auth_token, service_structure)
        except xmlrpc.client.Fault as err:
            if err.faultCode == 409:
                server.v1.libraries.service.update(auth_token, dict_services[service_name], service_structure)

server.v2.core.logout(auth_token)
