# niejx 搬运回wp 输出外链图片地址
# ol28b5m5b.bkt.clouddn.com 七牛地址
import os
import bs4
import lxml

wpurl = "https://puzzlendragon.wordpress.com"
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
        file = "src\\bleachgacha.html"
    else:
        file = srcfile

    with open(file,"r", encoding='utf-8') as htmlfile:
        raw = htmlfile.read()
    soup = bs4.BeautifulSoup(raw,'lxml')

    article = soup.find(class_='entry-content')
    if(article != None):
        if(article.find(class_='featured-image') != None):
            article.find(class_='featured-image').extract()
        alla = article.find_all('a')
        allimg = article.find_all('img')
        for ia in alla:
            ihref = ia['href']
            #print(ihref)
            if(ihref[0:2] =="./"):
                href = wpurl+ ihref[1:]
                if(href[-5:] == ".html"):
                    href = href[:-5]+"/"
                elif(href[-7:] == ".html?v"):
                    href = href[:-7] +"/"
                ihref = href
            elif(ihref[0:15] == "http://ol28b5m5b"):
                ihref = wpurl
            #print(ihref)
            ia['href'] = ihref
        for iimg in allimg:
            isrc = iimg['src']
            #print(isrc)
            if(isrc[0:2] == "./"):
                src = transurl + isrc[1:]
                iimg['src'] = src
            #print(iimg['src'])

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
        filename, ext = os.path.splitext(savefile)
        savefile = filename + ".txt"
        with open(savefile, "w", encoding='utf-8') as newfile:
            newfile.write(str(article))


if __name__ == '__main__':
  main()