from display.handlers.base import BaseHandler

class TestHandler(BaseHandler):
    @web.asynchronous
    @gen.engine
    def get(self):
        title = 'list'
        self.render('index/data.html', title = title)

    def post(self):
        key = 'ip_queue_0'
        d = self.application.redis.lpop(key)
        logger = Log().getLogger('development')
        logger.info(d)
        db = self.application.conn
        cursor = db.cursor()
        sql = """select ip, port, scheme, level, flag, times, create_time, update_time  from `ip` order by update_time asc limit %s,%s """
        params = (0, 10)
        cursor.execute(sql, params)
        res = cursor.fetchall()

        client = httpclient.AsyncHTTPClient()
        li = []
        if res:
            for value in res:
                ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int(value[0]))))
                data = {'ip' : ip, 'port' : value[1], 'scheme' : value[2], 'level' : value[3], 'flag':value[4], 'times' : value[5], 'create_time': value[6], 'update_time' : value[7]}
                response = yield gen.Task(client.fetch, "http://ip.taobao.com/service/getIpInfo.php?ip=" + ip)
                info = json.loads(response.body.decode('utf-8'))
                if info['code'] == 0:       
                    data['isp'] = info['data']['isp']
                    data['city'] = info['data']['city']
                    data['area'] = info['data']['area']
                    data['region'] = info['data']['region']
                    data['country'] = info['data']['country']
                li.append(data)
        return json.dumps(li)
