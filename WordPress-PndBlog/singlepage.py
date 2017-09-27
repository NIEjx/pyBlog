import os
from queue import Queue
import re
import time
import threading
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import lxml

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
url = "https://puzzlendragon.wordpress.com/2016/08/31/dungeon/"

transurl = "http://ol28b5m5b.bkt.clouddn.com"
name = "singlemulti.html"

print("start page ", url)
with urllib.request.urlopen(url, timeout=30) as htmlpage:
    html = htmlpage.read()
# find out all sub pages
all_self = re.findall("\"(" + url + "[\d]+/[\d]+/[\d]+/[\w\.\-]*/)\"", str(html))
# for i in all_self:
#     if (inhtmllist(i) == False):
#         tmpname = i.split('/')[-2] + ".html"
#         htmlQueue.append(i)
#         workQueue.put(pageName(i, tmpname))

soup = BeautifulSoup(html, "lxml")
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
        print(iimg)
    src = str(tmpsrc).split('/')[-1]
    iimg['src'] =  "./img/" + name.split('.')[-2] + "/" + src
for i in sitecontent.find_all("div", class_="sharedaddy"):
    i.extract()
for i in sitecontent.find_all("div", class_="wpcnt"):
    i.extract()
sitecontent.find("footer").extract()
# 处理链接
menu = "<div class=\"menu-container\" id=\"menu\"><a alt=\"Menu\" href=\"./menu.html\" rel=\"home\">Menu</a></div>"
prefix = "<div id=\"content\" class=\"site-content\">\n"
subfix = "<div id=\"copyright\"><span><br><br><br>Copyright © 1988-2020 Nie.jx. All rights reserved.</span></div></div>\n"
tmpsrc = htmlprefix + \
         str(sitetitle) + "\n" + menu + "\n" + prefix + str(sitecontent) \
         + subfix + htmlsubfix

soup = BeautifulSoup(tmpsrc, "lxml")
alla = soup.find_all("a")
count = 0
for ia in alla:
    istr = ia['href']
    if (istr == url):
        ia['href'] = transurl
    elif (istr[0] != "#"):
        try:
            itmp = istr.split('/')[-2]
        except:
            print(istr)
        if (itmp.find('.') < 0 and itmp.find('%') < 0):
            ia['href'] = "./" + itmp + ".html"
        else:
            print(ia)
            count += 1
print(soup)