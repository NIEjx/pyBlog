# 自动去掉style 加上link的css
import os
import re
import time
from datetime import datetime
from PIL import Image
import threading
import urllib.request
import urllib.error
import bs4
#replace url to start your own download
url = "https://pad.gungho.jp/member/index.html"
url_prefix = "https://pad.gungho.jp/member/"
urle_prefix = "https://pad.gungho.jp/member/event/"

dirname = os.getcwd()
print_lock = threading.Lock()

htmlprefix = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="智龙迷城攻略" property="og:title"/>
<meta content="分享游戏的系统介绍和攻略" property="og:description"/>
<meta content="智龙迷城攻略" property="og:site_name"/>
<meta content="智龙迷城，pad,puzzleanddragon，pnd，游戏攻略" name="keywords"/>
<meta content="智龙迷城，pad,puzzleanddragon，pnd，游戏攻略，分享游戏的系统介绍和攻略" name="description"/>
<link href="./img/ico.png" rel="icon" sizes="16x16" type="image/x-icon"/>
<link rel="stylesheet" id="allcss" href="./1.css" type="text/css" media="all">
<title>智龙迷城攻略 – 日服（及港台服）攻略分享</title>
</head>
<body>
<div class="site-branding">
<h1 class="site-title"><a alt="智龙迷城攻略" href="http://ol28b5m5b.bkt.clouddn.com" rel="home">智龙迷城攻略</a></h1>
<h2 class="site-description">日服（及港台服）攻略分享</h2>
</div>
<div class="menu-container" id="menu"><a alt="Menu" href="./menu.html" rel="home">Menu</a></div>
<div class="site-content" id="content">
<article class="post-1 page type-page status-publish hentry" id="post-1">
<header class="entry-header">
<h3 class="entry-title">最新活动</h3>'''
htmlmiddle = '''</header><!-- .entry-header -->
<div class="entry-content">
<div class="featured-image">
</div>'''
htmlsubfix = '''</div><!-- .entry-content -->
<!-- .entry-footer -->
</article><div id="copyright"><span><br><br><br>Copyright © 1988-2020 Nie.jx. All rights reserved.</span></div></div><script type="text/javascript">
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
cprefix = ''''''
csubfix = ''''''

MaxThread = 40

def getEvent(eventurl):
    with urllib.request.urlopen(eventurl) as html:
        raw = html.read()
    all_event = []
    soup = bs4.BeautifulSoup(raw,"html.parser")
    all_time = soup.find_all(class_='day')
    for i in all_time:
        tagtitle = i.previous_sibling
        if(tagtitle.name != "div"):
            tagtitle = i.previous_sibling.previous_sibling
        tagimg = i.next_sibling
        if(tagimg!="div"):
            tagimg = i.next_sibling.next_sibling
        tmpimg = tagimg.find('img')
        img = saveEImg(tmpimg['src'], "img\\event")
        if (img != False):
            tmpsrc = "<dl><dt>" + tagtitle.text + "</dt>\n<dd>"
            tmpsrc += i.text + "</dd>\n<dd>"
            tmpsrc += "<img src=\"./img/event/" + img + "\"/></dd></dl>"
            all_event.append(tmpsrc)
        else:
            print("no img " + tmpimg['src'])
            tmpsrc = "<dl><dt>" + tagtitle.text + "</dt>\n<dd>"
            tmpsrc += i.text + "</dd>\n<dd>"
            tmpsrc += "没找到图片</dd></dl>"
            all_event.append(tmpsrc)
    return all_event

def getSPD(spdurl):
    with urllib.request.urlopen(spdurl) as html:
        raw = html.read()
    all_spd = ""
    soup = bs4.BeautifulSoup(raw,"html.parser")
    all_time = soup.find_all(class_='green')
    for i in all_time:
        all_spd +=  "<br>" + i.text
    return all_spd


def mkdir(path):
    tmppath = os.getcwd()+"\\"+path
    try:
        os.makedirs(tmppath)
    except:
        print("DIR exist!")
        exit()
    return tmppath

# save and resize image
def saveImg(imgUrl,dir):
    time.sleep(0.1)
    with print_lock:
        tdir = os.getcwd() + "\\" + dir
        if(os.path.exists(tdir) == False):
            print(tdir)
            mkdir(dir)
        names = imgUrl.split('/')
        imgName = ""
        for i in names[1:]:
            imgName += i
        if(imgUrl[0:2] == ".."):
            tmpimgurl = url_prefix + imgUrl[3:]
        else:
            tmpimgurl = url_prefix + imgUrl
        try:
            with urllib.request.urlopen(tmpimgurl) as imghtml:
                rawimg = imghtml.read()
                with open(tdir+"\\"+imgName,'wb') as file:
                    file.write(rawimg)
                tmpimg = Image.open(tdir+"\\"+imgName, 'r')
                width, height = tmpimg.size
                if (width > 300):
                    tmpimg.thumbnail((300, 300.0 * height / width), Image.ANTIALIAS)
                time.sleep(0.1)
                tmpimg.save(tdir+"\\"+imgName, optimize=True, quality=85)
                return imgName
        except OSError as err:
            print("OS error: {0}".format(err))
            return False

# save and resize image
def saveEImg(imgUrl,dir):
    time.sleep(0.1)
    with print_lock:
        tdir = os.getcwd() + "\\" + dir
        if(os.path.exists(tdir) == False):
            print(tdir)
            mkdir(dir)
        names = imgUrl.split('/')
        imgName = ""
        for i in names[1:]:
            imgName += i
        if(imgUrl[0:2] == ".."):
            tmpimgurl = url_prefix + imgUrl[3:]
        else:
            tmpimgurl = urle_prefix + imgUrl
        try:
            with urllib.request.urlopen(tmpimgurl) as imghtml:
                rawimg = imghtml.read()
                with open(tdir+"\\"+imgName,'wb') as file:
                    file.write(rawimg)
                tmpimg = Image.open(tdir+"\\"+imgName, 'r')
                width, height = tmpimg.size
                if (width > 300):
                    tmpimg.thumbnail((300, 300.0 * height / width), Image.ANTIALIAS)
                time.sleep(0.1)
                tmpimg.save(tdir+"\\"+imgName, optimize=True, quality=85)
                return imgName
        except OSError as err:
            print("OS error: {0}".format(err))
            return False

def main():
    today = datetime.now()
    start = time.time()
#----------------------------------
    with urllib.request.urlopen(url) as html:
        raw = html.read()
    all_code = []
    soup = bs4.BeautifulSoup(raw,"html.parser")
    all_pages = soup.findAll('div',id='banner_block_dodai')[0]
    all_events = all_pages.findAll('dt')
    for dt in all_events:
        i = dt.find('a')
        #print(i['href'])
        if(i['href'][0:5]=="event"):
            #print(i['href'])
            #print(i.parent.parent)
            tmpimg = i.parent.parent.find('img')
            datetag = i.parent.parent.find(class_='cartegoryDate')
            if(datetag == None):
                datetag = i.parent.parent.find('dd')
            tmpdate = datetag.text
            img = saveImg(tmpimg['src'],"img\\event")
            if(img != False):
                tmpimg['src'] = "./img/event/"+ img
                tmpsrc = "<dl><dt>"+ str(tmpimg['alt']) + "</dt>\n<dd>"
                tmpsrc += tmpdate + "</dd>\n<dd>" + str(tmpimg) + "</dd></dl>"
                all_code.append(tmpsrc)
            else:
                print("no img "+ str(tmpimg['alt']))
                tmpsrc = "<dl><dt>"+ str(tmpimg['alt']) + "</dt>\n<dd>"
                tmpsrc += tmpdate + "</dd>\n<dd>没找到图片</dd></dl>"
                all_code.append(tmpsrc)
            if (i['href'][6:12] != "godfes"):
                #print(i.parent.parent)
                tmpurl = url_prefix+i['href']
                tmpsrc = getEvent(tmpurl)
                for i in tmpsrc:
                    all_code.append(i)
        elif(i['href'][0:7]=="collabo"):
            #print(i.parent.parent)
            tmpimg = i.parent.parent.find('img')
            datetag = i.parent.parent.find(class_='cartegoryDate')
            if (datetag == None):
                datetag = i.parent.parent.find('dd')
            tmpdate = datetag.text

            img = saveImg(tmpimg['src'],"img\\rare")
            if (img != False):
                tmpimg['src'] = "./img/rare/" + img
                tmpsrc = "<dl><dt>"+ str(tmpimg['alt']) + "</dt>\n<dd>"
                tmpsrc += tmpdate + "</dd>\n<dd>" + str(tmpimg) + "</dd></dl>"
                all_code.append(tmpsrc)
            else:
                print("no img "+ str(tmpimg['alt']))
                tmpsrc = "<dl><dt>"+ str(tmpimg['alt']) + "</dt>\n<dd>"
                tmpsrc += tmpdate + "</dd>\n<dd>没找到图片</dd></dl>"
                all_code.append(tmpsrc)
        elif (i['href'][0:5] == "quest" or i['href'][0:6] == "advent" or i['href'][0:7] == "ranking" or i['href'][0:5] == "carni"):
            # print(i.parent.parent)
            tmpimg = i.parent.parent.find('img')
            datetag = i.parent.parent.find(class_='cartegoryDate')
            if (datetag == None):
                datetag = i.parent.parent.find('dd')
            tmpdate = datetag.text

            img = saveImg(tmpimg['src'], "img\\event")
            if (img != False):
                tmpimg['src'] = "./img/event/" + img
                tmpsrc = "<dl><dt>" + str(tmpimg['alt']) + "</dt>\n<dd>"
                tmpsrc += tmpdate + "</dd>\n<dd>" + str(tmpimg) + "</dd></dl>"
                all_code.append(tmpsrc)
            else:
                print("no img " + str(tmpimg['alt']))
                tmpsrc = "<dl><dt>" + str(tmpimg['alt']) + "</dt>\n<dd>"
                tmpsrc += tmpdate + "</dd>\n<dd>没找到图片</dd></dl>"
                all_code.append(tmpsrc)
        elif (i['href'][0:3] == "sp_"):
            # print(i.parent.parent)
            tmpimg = i.parent.parent.find('img')
            datetag = i.parent.parent.find(class_='cartegoryDate')
            if (datetag == None):
                datetag = i.parent.parent.find('dd')
            tmpdate = datetag.text

            if( re.findall("series", str(i['href'])) !=[] ):
                tmpurl = url_prefix+i['href']
                tmpdate = tmpdate + getSPD(tmpurl)

            img = saveImg(tmpimg['src'], "img\\event")
            if (img != False):
                tmpimg['src'] = "./img/rare/" + img
                tmpsrc = "<dl><dt>" + str(tmpimg['alt']) + "</dt>\n<dd>"
                tmpsrc += tmpdate + "</dd>\n<dd>" + str(tmpimg) + "</dd></dl>"
                all_code.append(tmpsrc)
            else:
                print("no img " + str(tmpimg['alt']))
                tmpsrc = "<dl><dt>" + str(tmpimg['alt']) + "</dt>\n<dd>"
                tmpsrc += tmpdate + "</dd>\n<dd>没找到图片</dd></dl>"
                all_code.append(tmpsrc)

        #     print(i.parent.parent)
    print(len(all_events))

    tmpsrc = htmlprefix
    tmpsrc = tmpsrc + "<span>Posted on " + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "</span>\n" +htmlmiddle
    for i in all_code:
        tmpsrc += i
    tmpsrc += htmlsubfix
    with open("weekevent.html", "w", encoding='utf-8') as htmlfile:
        htmlfile.write(tmpsrc)
    print("entire job took:", time.time()-start)

if __name__ == '__main__':
  main()

  # # 暂时不加入年判断 如果结束日早于今天的话，去掉该活动
  # startm = startd = endd = endm = 0
  # if(tmpdate[2]=='/'):
  #     startm = int(tmpdate[0:2])
  #     startd = int(tmpdate[3:5])
  #     if(tmpdate[16]=='/'):
  #         endm = int(tmpdate[14:16])
  #         endd = int(tmpdate[17:19])
  #     elif(tmpdate[18]=='/' and tmpdate[21]=='/'):
  #         endm = int(tmpdate[19:21])
  #         endd = int(tmpdate[22:24])
  # elif(tmpdate[4]=='/' and tmpdate[7]=='/'):
  #     startm = int(tmpdate[5:7])
  #     startd = int(tmpdate[8:9])
  #     endm = int(tmpdate[24:26])
  #     endd = int(tmpdate[27:29])
  # print(startm,startd,endm,endd)