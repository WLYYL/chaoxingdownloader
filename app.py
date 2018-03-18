import os

from crawler import BookDownloader
from pdf_merge import merge

try:
    os.makedirs('./下载/图片')
except FileExistsError:
    pass
    
while True:
    bd = BookDownloader(input('输入书籍阅读地址回车：'))
    print()
    if bd.main():
        merge(os.path.join('./下载/图片', bd.book))
    print()