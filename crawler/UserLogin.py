# -*- coding: utf-8 -*-  
import requests  
import base64  
import re  
import urllib  
import rsa  
import json  
import binascii  
import time
from scrapy import Selector
  
class Userlogin:  
    def userlogin(self,username='iou2much@sina.com',password='',pagecount=1):  
        session = requests.Session()  
        url_prelogin = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.5)&_=%s'%(int(time.time()*1000))
        url_login = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'  
  
        #get servertime,nonce, pubkey,rsakv  
        resp = session.get(url_prelogin)  
        json_data  = re.search('\((.*)\)', resp.content).group(1)  
        data       = json.loads(json_data)  
        servertime = data['servertime']  
        nonce      = data['nonce']  
        pubkey     = data['pubkey']  
        rsakv      = data['rsakv']  
  
        # calculate su  
        su  = base64.b64encode(urllib.quote(username))  
  
        #calculate sp  
        rsaPublickey= int(pubkey,16)  
        key = rsa.PublicKey(rsaPublickey,65537)  
        message = str(servertime) +'\t' + str(nonce) + '\n' + str(password)  
        sp = binascii.b2a_hex(rsa.encrypt(message,key))  
        postdata = {  
                            'entry': 'weibo',  
                            'gateway': '1',  
                            'from': '',  
                            'savestate': '7',  
                            'userticket': '1',  
                            'ssosimplelogin': '1',  
                            'vsnf': '1',  
                            'vsnval': '',  
                            'su': su,  
                            'service': 'miniblog',  
                            'servertime': servertime,  
                            'nonce': nonce,  
                            'pwencode': 'rsa2',  
                            'sp': sp,  
                            'encoding': 'UTF-8',  
                           'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',  
                            'returntype': 'META',  
                            'rsakv' : rsakv,  
                            }  
        resp = session.post(url_login,data=postdata)  
        #print resp.headers  
        #print resp.content
        #login_url = re.findall('replace\(\'(.*)\'\)',resp.content)  
        login_url = re.findall('replace\(\"(.*)\"\)',resp.content)  
        #print login_url 
        #  
        respo = session.get(login_url[0])  
        print respo.headers  
        print respo.content
        uid = re.findall('"uniqueid":"(\d+)",',respo.content)[0]  
        url = "http://weibo.com/u/"+uid  
        respo = session.get(url)  
        # print respo.content #获取首页的内容html  
#以上为成功登陆微博  
        myheaders={}  
        myheaders['set-cookie'] = resp.headers['set-cookie']  
        myheaders['Referer'] = 'http://weibo.com/ioumuch/home?leftnav=1&wvr=5'
#以下是开始抓取信息  
        for i in range(6,int(pagecount)+1):  
            allfeeds = []
            json_file = open('%s.json'%i,'w')
            forwardUrl = """http://weibo.com/fav?page=%d"""%i
            r = session.post(forwardUrl,headers=myheaders)
            page = r.content
            #print page
            #sel = HtmlXPathSelector(text=page)
            sel = Selector(text=page)
            #div = sel.xpath('//div[@node-type="favContent"]')
            scripts = sel.xpath('//script/text()')
            script = ''
            for s in scripts:
                #print s.extract()
                if u'收藏list' in s.extract():
                    script = s.extract()

            #print script[41:-1]
            div = Selector(text=json.loads(script[41:-1])['html'])
            feeds = div.xpath('//div[@class="WB_feed"]/div')
            print 'got %s !!'%i
            
            for f in feeds :
                #print feed
                feed = {}
                detail = f.xpath('div/div[@class="WB_detail"]')
                user   = detail.xpath('div[@class="WB_info"]/a[1]/text()')
                if not user:continue
                feed['user'] = detail.xpath('div[@class="WB_info"]/a[1]').extract()[0]
                feed['text'] = detail.xpath('div[@class="WB_text"]').extract()[0]

                feed['media'] = detail.xpath('*[@node-type="feed_list_media_prev"]').extract()
                if feed['media']:
                    feed['media']=feed['media'][0]
                else:
                    feed['media']=''

                feed['forward'] = detail.xpath('div[@node-type="feed_list_forwardContent"]').extract()
                if feed['forward']: 
                    feed['forward'] = feed['forward'][0]
                else:
                    feed['forward'] = ''
                allfeeds.append(feed)
                #print feed
            json_file.write(json.dumps(allfeeds))
