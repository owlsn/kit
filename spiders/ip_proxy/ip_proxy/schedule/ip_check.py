# coding = utf-8
import sys
import os
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(p)
from ip_proxy.connection.mysql_connection import MysqlConnection
from ip_proxy.utils.ip_tools import IpTools
import json
import socket
import struct

if __name__ == '__main__':
    tool = IpTools()
    mysql = MysqlConnection(type = 'syn')
    conn = mysql.conn
    cursor = conn.cursor()
    sql = """select ip,port from `ip` limit 0,10"""
    cursor.execute(sql)
    res = cursor.fetchall()
    for value in res:
        ip = socket.inet_ntoa(struct.pack('I',socket.htonl(value[0])))
        port = value[1]
        r = tool.ip_check(ip, port)