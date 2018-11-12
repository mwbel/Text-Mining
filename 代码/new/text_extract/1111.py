# coding: utf-8
import fitz


doc=fitz.open('E:/pic/3/广发证券/20180809-广发证券-免税行业专题报告之全球机场免税详解：龙头规模扩大提升盈利，东南亚机场持续高增长/20180809-广发证券-免税行业专题报告之全球机场免税详解：龙头规模扩大提升盈利，东南亚机场持续高增长.pdf')
page=doc[24]
word=page.getText()

# print(word.decode('UTF-8').encode('GBK'))
print(page.searchFor('表 10'))