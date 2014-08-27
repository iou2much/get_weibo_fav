# -*- encoding:utf-8 -*-  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from UserLogin import Userlogin;  
  
def menuChoice():  
    username = raw_input("输入新浪微博账号：")  
    password = raw_input("输入密码：")  
    pagecount = raw_input("输入想要抓取评论的页数：")  
    o = Userlogin()  
    o.userlogin(username=username,password=password, pagecount=pagecount)  
    print "抓取完毕"  
menuChoice() 
