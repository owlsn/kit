from display.handlers.base import BaseHandler
import socket
import struct
import json

class TablesDataHandler(BaseHandler):
    def get(self):
        title = 'TablesDataHandler'
        self.render('tables/data.html', title = title, **self.render_dict)

    def post(self):
        page = self.get_argument('page', 1)
        limit = self.get_argument('limit', 10)
        start = self.get_argument('start', 0)

        # db = self.application.conn
        # cursor = db.cursor()
        # sql = """select ip, port, scheme, level, flag, times, create_time, update_time  from `ip` order by update_time asc limit %s,%s """
        # params = (int(start), int(limit))
        # count_sql = """select count(*) as count  from `ip` """
        # cursor.execute(sql, params)
        # res = cursor.fetchall()

        # r = cursor.execute(count_sql)
        # result = cursor.fetchone()
        # total = result[0]
        # li = []
        # if res:
        #     for value in res:
        #         ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int(value[0]))))
        #         data = {'ip' : ip, 'port' : value[1], 'scheme' : value[2], 'level' : value[3], 'flag':value[4], 'times' : value[5], 'create_time': value[6], 'update_time' : value[7]}
        #         li.append(data)
        li = []
        total = 0
        data = {
            'page' : page,
            'start' : start,
            'limit' : limit,
            'data' : li,
            'total' : total
        }
        self.write(json.dumps(data))