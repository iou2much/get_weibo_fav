# -*- encoding:utf-8 -*-  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from UserLogin import Userlogin;  
  
def menu():  
    print""" 
        选择你想要的功能： 
        0,退出 
        1,登陆微博并抓取评论 
    """

def menuChoice():  
    #choice = raw_input("输入你的选择（0/1）：")  
    choice = '1'
    while choice != '0':  
        if choice == '1':  
            #username = raw_input("输入新浪微博账号：")  
            password = raw_input("输入密码：")  
            pagecount = raw_input("输入想要抓取评论的页数：")  
            o = Userlogin()  
            o.userlogin(password=password, pagecount=pagecount)  
            #print "抓取完毕"  
            break
            #choice = raw_input("输入你的选择（0/1）：")  
        else:  
            print """choice=%s"""%choice  
            print "输入无效"  
            choice = raw_input("输入你的选择（0/1/2/3）：")  
 
#menu()  
menuChoice() 
