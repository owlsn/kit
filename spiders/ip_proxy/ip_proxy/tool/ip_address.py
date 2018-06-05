# coding = utf-8

import requests

class IpAddress(object):
    
    def info(ip):
        if ip == None:
            return None
        else:
            url = 'http://ip.taobao.com//service/getIpInfo.php?ip=' + ip
            r = requests.get(url)
            return r.json()
            
