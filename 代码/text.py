import fitz
import re 

doc=fitz.open('/Users/Pro/Documents/Others/应用项目/Text Mining/待处理/201808/未处理的报告/# 20180813-广发证券-商业贸易行业：阿里巴巴：缔造在线商业生态，迈向全球互联网巨头.pdf')
page=doc.loadPage(0)
Blocks=page.getTextBlocks(images=True)#提取page中的block
#Words=page.getTextWords(images=True)#提取page中的words
for a in Blocks:
    print(a)
# print(doc.pageCount)
# print(page.getText())#提取整个页面的文字
