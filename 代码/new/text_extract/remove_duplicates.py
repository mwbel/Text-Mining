import fitz
import os
from operator import itemgetter
def remove_dulipicates(path):
    # for file in os.listdir(path):
        # doc = fitz.open(os.path.join(path,file))
    doc = fitz.open("E:/项目/试运行/201808/需求4/处理完成/")
    page_count = doc.pageCount
    for i in range(page_count):
        page = doc[i]

        words = page.getTextWords()
        words.sort(key = itemgetter(1,0))

        y = words[0][1]
        x = words[0][0]

        oldrect = None
        lines = []
        line = ""
        for w in words:
            newrect = fitz.Rect(w[:4])
            if newrect == oldrect:
                continue
            oldrect = newrect
            word = w[4]
            if newrect.y0 == y:
                line += word
                line += " "
            else:
                lines.append([x, y, line])
                line = word + " "
                y = newrect.y0
                x = newrect.x0

        lines.append([x, y, line])
        # we acknowledge, that the page effectively has 2 columns:
        for x0, y0, line in lines:
            space = ""
            if x0 > 180:
                space = " " * 60
            print(space + line)