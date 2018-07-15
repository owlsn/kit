# coding = utf-8

import requests
from ip_proxy.utils.log import Log

class IpTools(object):
    
    
    # 从ip.taobao.com获取地址以及运营商信息
    # params:ip
    # return:None|json
    def info(self,ip):
        if ip:
            url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
            r = requests.get(url, timeout = 30)
            return r.json()
        else:
            return None
        pass
        
            
