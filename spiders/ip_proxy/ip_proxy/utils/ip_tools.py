# coding = utf-8

import scrapy
import requests
import traceback
from ip_proxy.utils.log import Log

class IpTools(object):
    
    
    # 从ip.taobao.com获取地址以及运营商信息
    # params:ip
    # return:None|json
    def info(self,ip):
        if ip:
            url = 'http://ip.taobao.com//service/getIpInfo.php?ip=' + ip
            r = requests.get(url, timeout = 5)
            return r.json()
        else:
            return None
        pass

    # 检测代理的可用性
    # params:ip,port
    # return:false|dict
    def ip_check(self, ip, port, protocol = 'http'):
        try:
            host = ip
            protocol = protocol
            proxy = {
                protocol : host + ':' + str(port)
            }
            response = requests.get('http://www.baidu.com', proxies = proxy, timeout = 5)
            return response
            pass
        except Exception as e:
            logger = Log().getLogger('development')
            logger.info('test')
            pass
        
            
