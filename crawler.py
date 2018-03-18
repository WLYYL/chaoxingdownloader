import logging
import os
import re
import time
import hashlib
import urllib.request


class BookDownloader():
    POSTFIX = ('bok%03d', 'leg%03d', 'fow%03d', '!%05d', '%06d', 'cov%03d')

    def __init__(self, url):
        self.url = url
        self.book = ''
        self.prefix = ''
        self.error_times = 0

    def parse_home(self):
        try:
            r = urllib.request.urlopen(self.url)
            if r.code != 200:
                logging.warn('HTTP %s' % r.code)
                return
            r = r.read().decode()
        except Exception as e:
            logging.error('网址请求错误！\n%s' % e)
        try:
            self.book = re.search(
                r'<head>[\s\S]+?<title>(.+?)</title>[\s\S]+?</head>', r).group(1)
            print(self.book)

            prefix = re.search(r'jpgPath:\s"(.+?)",', r).group(1)
            self.prefix = urllib.parse.urljoin(self.url, prefix)

            pages = eval(re.search(r'var pages = (.+?);', r).group(1))
            pages = pages[1:]
            pages.remove(pages[-2])
            _pages = []
            for p in pages:
                _pages.append(p[1])

            return _pages
        except AttributeError as e:
            logging.error(e)
            print('当前书不支持，请换书')

    def url_join(self, postfix_num, page_num):
        postfix = self.POSTFIX[postfix_num] % page_num
        url = urllib.parse.urljoin(self.prefix, postfix)
        return url, postfix

    def download(self, pic_url, picpath):
        if os.path.exists(picpath):
            return
        try:
            urllib.request.urlretrieve(pic_url, picpath)
            print('下载 %s' % os.path.split(picpath)[1])
            self.check_error(picpath)
        except ChaoXingError:
            os.remove(picpath)
            logging.error('下载的图片有错，如果该消息重复出现，请重启程序！：%s' % picpath)
            time.sleep(10)
            self.download(pic_url, picpath)
            return
        except Exception as e:
            logging.error('%s 下载错误！如果该消息重复出现，请重启程序！\n%s' % (picpath, e))
            time.sleep(10)
            self.download(pic_url, picpath)
            return
        time.sleep(0.5)

    def check_error(self, picpath):
        if os.path.getsize(picpath) == 17663:
            if self.hash_file(picpath) == '9bcaf3fe00d1c5c5f4fe16cd0db266c4':
                raise ChaoXingError

    def hash_file(self, filename):
        b = open(filename, 'rb').read()
        return hashlib.md5(b).hexdigest()

    def main(self):
        pages = self.parse_home()
        try:
            os.mkdir('./下载/图片/%s' % self.book)
        except:
            pass
        if not pages:
            return
        for i in range(6):
            total_page_num = pages[i]
            for page_num in range(1, total_page_num + 1):
                url, picname = self.url_join(i, page_num)
                picpath = os.path.join('./下载/图片/%s' % self.book, picname)
                self.download(url, picpath + '.png')
        return True


class ChaoXingError(Exception):
    pass


if __name__ == '__main__':
    while True:
        bd = BookDownloader(input('输入书籍阅读地址回车：'))
        print()
        bd.main()
