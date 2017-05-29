# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os

class BDTB:
    def __init__(self, baseURL, seeLZ):
        self.baseURL = baseURL
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.defaultTitle = u"百度贴吧"

    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u"连接百度贴吧失败，错误原因 ",e.reason
                return None

    def getTitle(self, page):
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def mkdir(self, path):
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    def getAllImgs(self, page):
        pattern = re.compile('<img class="BDE_Image" src="(.*?)"', re.S)
        images = re.findall(pattern, page)
        return images

    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

    def saveImgs(self, images, name):
        number = 1
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL, fileName)
            number += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        if pageNum == None:
            print u"URL已失效，请重试"
            return
        try:
            print u"该帖子共有" + str(pageNum) + u"页"
            for i in range(1, int(pageNum)+1):
                print u"正在保存第" + str(i) + u"页图片"
                page = self.getPage(i)
                images = self.getAllImgs(page)
                path = title + " " + str(i)
                self.mkdir(path)
                self.saveImgs(images, path)
        except IOError,e:
            print u"写入异常，原因" + e.message
        finally:
            print u"写入任务完成"

baseURL = 'http://tieba.baidu.com/p/2020041485'
seeLZ = raw_input(u"是否只获取楼主发言，是输入1，否输入0\n")
bdtb = BDTB(baseURL, seeLZ)
bdtb.start()


