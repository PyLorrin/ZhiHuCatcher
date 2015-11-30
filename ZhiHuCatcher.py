
# -*- coding: utf-8 -*-
import os,sys,time,socket 
reload(sys)
sys.setdefaultencoding('utf-8')
type = sys.getfilesystemencoding()
import urllib2, HTMLParser
from BeautifulSoup import BeautifulSoup

html_parser = HTMLParser.HTMLParser()

Category = ['collection/','topic/']
InputPageNum = raw_input("please choose type:\n[0]:collection\n[1]:topic\n") or '0'
PageType = Category[int(InputPageNum)]

IdNumBegin = int(raw_input('begin from?') or '27109279')
IdNumEnd = int(raw_input('end in?') or '20000000')

flog = open(sys.path[0]+'\log.ini','a')
flog.write(time.strftime('%Y-%m-%d',time.localtime(time.time()))+'\n')
for IntIdNum in range(IdNumBegin,IdNumEnd):
    IdNum = str(IntIdNum)
    url = "http://www.zhihu.com/"+ PageType + IdNum  #网址
    print 'try'+IdNum
    try:
        page = urllib2.urlopen(url,timeout=3)     #打开网页
        soup = BeautifulSoup(page)
    except urllib2.HTTPError,e:
        print '404\n'
        continue
    except urllib2.URLError:
        print 'timeout\n'
        continue
    except socket.error, arg:
        print "Connect server failed\n"
        continue
    except:
        print "error"
        continue

    flog.write(IdNum+': '+soup.title.string+'\n')
    
    QuestionsNum = 1
    try:
        f = open(sys.path[0]+'\\'+IdNum+soup.title.string.replace('/','or')+'.html','w')     #打开文件
    except:
        print "bad name!\n"
        continue
    f.write("""<!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>zhihu</title>
        <style type="text/css">
            img{
                width: 50%
            }
            
            *{
                font-family:"Arial","Microsoft YaHei","HeiTi","黑体","宋体",sans-serif;
            }
            
            p{
                line-height:100%
            }
            
        </style>
        
    </head>

    <body>""")
    if InputPageNum=='0':
        Maxpagenum=11
    else:
        Maxpagenum=2
    for pagenum in range(1,Maxpagenum):        #从第1页爬到第20页
        strpagenum = str(pagenum)      #页数的str表示
        print "Getting data for Page " + strpagenum   #shell里面显示的，表示已爬到多少页
        url = "http://www.zhihu.com/"+ PageType + str(IdNum) + "?page="+strpagenum  #网址
        try:
            page = urllib2.urlopen(url)     #打开网页
            soup = BeautifulSoup(page)      #用BeautifulSoup解析网页
        except:
            print "error"
            continue
        
        #找到具有class属性为下面两个的所有Tag
        if(InputPageNum=='0'):
            ALL = soup.findAll(attrs = {'class' : ['zm-item-title','content hidden'] }) #zh-summary summary clearfix
        else:
            ALL = soup.findAll(attrs = {'class' : ['question_link','content hidden'] })
        for each in ALL :               #枚举所有的问题和回答
            #print type(each.string)
            #print each.name
            if each.name == 'h2' :      #如果Tag为h2类型，说明是问题
                #print each.a.string     #问题中还有一个<a..>，所以要each.a.string取出内容
                if each.a.string:       #如果非空，才能写入
                    f.write("<h3>\n")
                    f.write(str(QuestionsNum) +'. ')
                    QuestionsNum += 1
                    f.write(each.a.string)
                    f.write("</h3>\n")
                else :                  #否则写"No Answer"
                    f.write("<p>\n")
                    f.write("No Answer")
                    f.write("</p>\n")
            elif each.name == 'a':
                #print each.string
                if each.string:       #如果非空，才能写入
                    f.write("<h3>\n")
                    f.write(str(QuestionsNum) +'. ')
                    QuestionsNum += 1
                    f.write(each.string)
                    f.write("</h3>\n")
                else :                  #否则写"No Answer"
                    f.write("<p>\n")
                    f.write("No Answer")
                    f.write("</p>\n")
            else :                      #如果是回答，同样写入
                print str(QuestionsNum)
                if each.string: 
                    f.write("<div>\n")
                    f.write("<p>\n")
                    f.write(html_parser.unescape(each.string))
                    f.write("</p>\n")
                    f.write("</div>\n")
                else :
                    f.write("<p>\n")
                    f.write("No Answer")
                    f.write("</p>\n")
    f.write("</body>")
    f.close()                           #关闭文件
flog.close()