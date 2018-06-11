# coding = utf-8

import requests

# 从ip.taobao.com获取地址以及运营商信息
class IpAddress(object):
    
    def info(ip):
        if ip:
            url = 'http://ip.taobao.com//service/getIpInfo.php?ip=' + ip
            r = requests.get(url)
            return r.json()
        else:
            return None
            
