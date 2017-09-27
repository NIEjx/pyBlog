# 增加link  css 标签去掉style
# ol28b5m5b.bkt.clouddn.com 七牛地址
import os
import bs4
import lxml


transurl = "http://ol28b5m5b.bkt.clouddn.com"

htmlQueue = []
logfile = []
refresh = []

def mkdir(path):
    try:
        os.makedirs(path)
    except:
        pass
    return path

def main(srcfile = None ,dstdir = None):
    if(srcfile == None):
        file = "src\\index.html"
    else:
        file = srcfile
    with open(file,"r", encoding='utf-8') as htmlfile:
        raw = htmlfile.read()
    soup = bs4.BeautifulSoup(raw,'lxml')
    # del style
    for i in soup('style'):
        i.extract()
    #insert link
    link = bs4.BeautifulSoup("<link rel=\"stylesheet\" id=\"allcss\" href=\"./1.css\" type=\"text/css\" media=\"all\">",'lxml')
    #print(link.link)
    soup.head.insert(14,link.link)

    if(dstdir == None):
        savefile = file.split('\\')[-1]
    else:
        offset = ""
        list = file.split('\\')
        if(len(list) != 1 ):
            for i in list[1:]:
                offset += "\\" + i
            savefile = dstdir + offset
        else:
            savefile = dstdir + file
    tdir, file = os.path.split(savefile)
    if (os.path.exists(tdir) == False):
        print(tdir)
        mkdir(tdir)
    with open(savefile, "w", encoding='utf-8') as newfile:
        newfile.write(str(soup))

    #     raw = htmlfile.readlines()
    # if(raw[9][0] == '<'):
    #
    # src = ""
    # for i in raw:
    #     src += i
    # print(src)

if __name__ == '__main__':
  main()