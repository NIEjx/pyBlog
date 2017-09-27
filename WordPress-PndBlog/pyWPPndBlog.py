# pnd攻略网搬家
# ol28b5m5b.bkt.clouddn.com 七牛地址
import os
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
from queue import Queue
import time
import threading
import lxml
import sys
sys.path.append('../pyPadHP')
import pyPadHp as padevent

MaxThread = 40
url = "https://puzzlendragon.wordpress.com/"
transurl = "http://ol28b5m5b.bkt.clouddn.com"

htmlQueue = []
logfile = []
refresh = []
workQueue = Queue()

htmlprefix = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta property="og:title" content="智龙迷城攻略" />
<meta property="og:description" content="分享游戏的系统介绍和攻略" />
<meta property="og:site_name" content="智龙迷城攻略" />
<meta name="keywords" content="智龙迷城，pad,puzzleanddragon，pnd，游戏攻略">
<meta name="description" content="智龙迷城，pad,puzzleanddragon，pnd，游戏攻略，分享游戏的系统介绍和攻略">
<link rel="icon" type="image/x-icon" href="./img/ico.png" sizes="16x16" />
<link rel="stylesheet" id="allcss" href="./1.css" type="text/css" media="all">
<title>智龙迷城攻略 &#8211; 日服（及港台服）攻略分享</title>
</head>
<body>\n'''
htmlsubfix = '''<script type="text/javascript">
var xhr = new XMLHttpRequest();

// 指定通信过程中状态改变时的回调函数
xhr.onreadystatechange = function(){
  //通信成功时，状态值为4
  if (xhr.readyState === 4){
    if (xhr.status === 200){
      var html = xhr.responseXML;
      //console.log(html);
      //console.log(xhr.responseText);
      if(html==null){
        var parser=new DOMParser();
        html=parser.parseFromString(xhr.responseText,"text/xml");
      }
      var target = document.getElementById('menu');
      //console.log(target);
      var menu = html.getElementById('menu').innerHTML;
      //console.log(menu);
      target.innerHTML = menu;
      //console.log(xhr.responseText);
    } else {
      console.error(xhr.statusText);
    }
  }
};
xhr.onerror = function (e) {
  console.error(xhr.statusText);
};
// var ajax = new XMLHttpRequest();
xhr.open('GET','./menu.html',true);
xhr.send(null);
</script>
</body></html>'''

def mkdir(path):
    tmppath = os.getcwd()+"\\"+path
    try:
        os.makedirs(tmppath)

    except:
        pass
    return tmppath
class pageName:
    url = ""
    name = ""
    def __init__(self, url, name):
        self.url = url
        self.name = name

def saveMenu(tmppage):
    try:
        #print("start page ", tmppage.url)
        with urllib.request.urlopen(tmppage,timeout=30) as htmlpage:
            html = htmlpage.read()
        soup = BeautifulSoup(html,"lxml")
        for iscript in soup('script'):
            iscript.extract()
        # 处理
        # 处理 div class
        menu = soup.find("nav").find("div")
        menu['class'] = "menu-container"
        menu['id'] = "menu"
        # 处理链接
        tmpsrc = htmlprefix +  str(menu) +"\n"+ "</body></html>"

        soup = BeautifulSoup(tmpsrc, "lxml")
        alla = soup.find_all("a")
        count = 0
        for ia in alla:
            istr = ia['href']
            if(istr == url):
                ia['href'] = transurl
            elif(istr[0] != "#"):
                try:
                    itmp = istr.split('/')[-2]
                except:
                    print(istr)
                if (itmp.find('.') < 0 and itmp.find('%') < 0):
                    ia['href'] = "./" + itmp + ".html"
                else:
                    count+=1
        logfile.append(tmppage + "\t未处理链接：\t"+str(count))
        with open("menu.html","w",encoding='utf-8') as htmlfile:
            htmlfile.write(str(soup))
    except OSError as err:
        print("OS error: {0}".format(err))
        logfile.append("Menu error in saving")
        pass

def savepage(tmppage):
    try:
        #print("start page ", tmppage.url)
        with urllib.request.urlopen(tmppage.url,timeout=30) as htmlpage:
            html = htmlpage.read()
        # find out all sub pages
        all_self = re.findall("\"(" + url + "[\d]+/[\d]+/[\d]+/[\w\.\-]*/)\"", str(html))
        for i in all_self:
            # if(i.split('/')[-2] =="kourin"):
            #     print("kourin")
            #     print(tmppage.url)
            if (inhtmllist(i) == False):
                tmpname = i.split('/')[-2]+".html"
                htmlQueue.append(i)
                workQueue.put(pageName(i,tmpname))

        soup = BeautifulSoup(html,"lxml")
        for iscript in soup('script'):
            iscript.extract()
        # 处理
        sitetitle = soup.find(class_="site-branding")
        # 处理 div class
        # menu = soup.find("nav").find("div")
        # menu['class'] = "menu-container"
        # content 处理图片 删除最后
        sitecontent = soup.find("article")
        allimg = sitecontent.find_all("img")
        # print(soup.img.name)
        for iimg in allimg:
            strs = []
            for iattr in iimg.attrs:
                strs.append(iattr)
            for istr in strs:
                if (istr != 'src'):
                    if (istr != 'width'):
                        del iimg[istr]
            try:
                tmpsrc = iimg['src']
            except:
                print(tmppage.url)
                print(iimg)
            src = str(tmpsrc).split('/')[-1]
            iimg['src'] = "./img/"+ tmppage.name.split('.')[-2] +"/"+ src
        for i in sitecontent.find_all("div",class_="sharedaddy"):
            i.extract()
        for i in sitecontent.find_all("div",class_="wpcnt"):
            i.extract()
        sitecontent.find("footer").extract()
        # 处理链接
        menu = "<div class=\"menu-container\" id=\"menu\"><a alt=\"Menu\" href=\"./menu.html\" rel=\"home\">Menu</a></div>"
        prefix = "<div id=\"content\" class=\"site-content\">\n"
        subfix = "<div id=\"copyright\"><span><br><br><br>Copyright © 1988-2020 Nie.jx. All rights reserved.</span></div></div>\n"
        tmpsrc = htmlprefix + \
                 str(sitetitle) +"\n" + menu +"\n"+ prefix + str(sitecontent) \
                 + subfix + htmlsubfix

        soup = BeautifulSoup(tmpsrc, "lxml")
        alla = soup.find_all("a")
        count = 0
        for ia in alla:
            istr = ia['href']
            if(istr == url):
                ia['href'] = transurl
            elif(istr[0] != "#"):
                try:
                    itmp = istr.split('/')[-2]
                except:
                    print(istr)
                if (itmp.find('.') < 0 and itmp.find('%') < 0):
                    ia['href'] = "./" + itmp + ".html"
                else:
                    #print(ia)
                    count+=1
        logfile.append(tmppage.url + "\t未处理链接：\t"+str(count))
        refresh.append(transurl + "/" + tmppage.name)
        with open(tmppage.name,"w",encoding='utf-8') as htmlfile:
            htmlfile.write(str(soup))
        # soup = BeautifulSoup(tmpsrc, "lxml")
        # alla = soup.find_all("a")
        # for ia in alla:
        #     istr = ia['href']
        #     itmp = istr.split('/')[-2]
        #     if (itmp.find('.') < 0 and itmp.find('%') < 0):
        #         ia['href'] = "http://" + transurl+"/"+itmp + ".html?v"
        # with open("qiniu\\"+tmppage.name,"w",encoding='utf-8') as htmlfile:
        #     htmlfile.write(str(soup))
        print( tmppage.url + " done")
    except OSError as err:
        print("OS error: {0}".format(err))
        print("page",tmppage.url)
        logfile.append(tmppage.url+"\t error in saving")
        pass



def inhtmllist(string):
    for istr in htmlQueue:
        if(istr == string):
            return True
    return False

def worker():
    while True:
        tmpPage = workQueue.get()
        savepage(tmpPage)
        workQueue.task_done()

def main():
    #socket.setdefaulttimeout(10)
    for x in range(MaxThread):
        t = threading.Thread(target = worker)
        t.daemon = True
        t.start()
    start = time.time()

    tmpdirname = re.findall(r'[\w\d%-\.]+',url)
    dirname = "not found"
    for i in tmpdirname:
        if(i.lower() != "http"):
            if(i.lower() != "https"):
                dirname = i
    os.chdir(mkdir(dirname))
    # mkdir("qiniu")
    htmlQueue.append(url)

    workQueue.put(pageName(url, "index.html"))
    saveMenu(url)
    workQueue.join()
    padevent.main()
    mkdir("log")
    with open("log\\html.txt","w",encoding='utf-8') as htmlfile:
        for ihtml in htmlQueue:
            htmlfile.write(str(ihtml)+"\n")

    with open("log\\log.txt","w",encoding='utf-8') as htmlfile:
        for ihtml in logfile:
            htmlfile.write(str(ihtml)+"\n")
    with open("log\\refresh.txt","w",encoding='utf-8') as htmlfile:
        for ihtml in refresh:
            htmlfile.write(str(ihtml)+"\n")
    print("entire job took:", time.time()-start)

    with open("log\\nie-root.html", "w", encoding='utf-8') as htmlfile:
        htmlfile.write("<html><body>")
        for ifile in os.listdir(os.getcwd()):
            htmlfile.write("<a href=\"./"+str(ifile) +"\">"+str(ifile)+"</a><br>\n")
        htmlfile.write("</body></html>")

if __name__ == '__main__':
  main()