# pnd攻略网搬家
# ol28b5m5b.bkt.clouddn.com 七牛地址
import os
import bs4
import lxml
import sys
sys.path.append(".")
# add link css instead of inbuild css
import pyAddlink as addlink
# remove ?v parameter
import pyRenew as renew
# convert niejx html version to wordpress
import pyToWP as towp


transurl = "http://ol28b5m5b.bkt.clouddn.com"

src_dir = "src"
dst_dir = "dst"

def mkdir(path):
    try:
        os.makedirs(path)
    except:
        pass
    return path

def ishtml(path):
    ext = path.split('.')[-1].lower()
    if(ext == 'html' or ext == 'htm'):
        return True
    else:
        return False

def main():
    images = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            str1 = os.path.join(root,file)
            if(os.path.isfile(str1)):
                if(ishtml(str1)):
                    images.append(str1)
    mkdir(dst_dir)
    for iimg in images:
        print(iimg)
        towp.main(iimg, dst_dir)


if __name__ == '__main__':
  main()