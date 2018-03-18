import os

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def merge(bookpath):
    print('合并中...')
    pagesize = _get_size(bookpath)
    try:
        os.mkdir('./下载')
    except:
        pass
    c = canvas.Canvas('./下载/%s.pdf' % os.path.split(bookpath)[1], pagesize=pagesize)
    
    for pic in _order_pic(bookpath):
        img = ImageReader()
        c.drawImage(img, 0, 0)
        c.showPage()
        # img = Image.open(os.path.join(bookpath,pic))
        # c.drawInlineImage(img,0,0)
        # c.showPage()
    c.save()
    print('合并完成!PDF文件在%s' % os.path.abspath('./下载'))

def _order_pic(bookpath):
    POSTFIX = ('bok',  'leg', 'fow', '!00', '000', 'cov')
    pics = [i for i in os.listdir(bookpath)]
    ordered_pics = sorted(pics, key=lambda x: [x.startswith(i) for i in POSTFIX],reverse = True)
    return ordered_pics

def _get_size(bookpath):
    max_width = max_height = 0
    for i in os.listdir(bookpath):
        png = os.path.join(bookpath, i)
        img = Image.open(png)
        if img.width > max_width:
            max_width = img.width
        if img.height > max_height:
            max_height = img.height
    return max_width, max_height