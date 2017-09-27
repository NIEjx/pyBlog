# 去掉？v参数
# ol28b5m5b.bkt.clouddn.com 七牛地址
import os
import bs4
import lxml


transurl = "http://ol28b5m5b.bkt.clouddn.com"

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
    print(file)
    with open(file,"r", encoding='utf-8') as htmlfile:
        raw = htmlfile.read()
    soup = bs4.BeautifulSoup(raw,'lxml')
    # del style
    for a in soup.find_all('a'):
        href = a['href']
        print(href)
        if(href[-2] == '?' and href[-1] == 'v'):
            num = len(href)
            a['href'] = href[0:num-2]
        print(a['href'])

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