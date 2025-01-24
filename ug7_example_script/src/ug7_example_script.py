#!/usr/bin/env python3

import xmlrpc.client
from pprint import pprint

SERVER = '192.168.84.26'
USER = 'API_Admin' 	
PASSWORD = 'Sup3rS#cretP@ssword!'

server = xmlrpc.client.ServerProxy('http://' + SERVER + ':4040/rpc', verbose=False)

res = server.v2.core.login(USER, PASSWORD, {})
auth_token = res['auth_token']
fw_rules = server.v1.firewall.rules.list(auth_token, 0, 100, {})
#pprint(fw_rules) #вывести до 100 правил

service_id = fw_rules['items'][0]['services'][0][1]
service = server.v1.libraries.service.fetch(auth_token, service_id)
pprint(service)   #вывести первый сервис из первого правила


server.v2.core.logout(auth_token)