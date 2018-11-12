# import fitz

# doc = fitz.open("E:/项目/试运行/201808/1/111.pdf")
# page = doc[0]
# d = page.getText("dict")
# for i in range(4,len(d['blocks'])):
#     print(d['blocks'][i])
#     # print(d['blocks'][i]['lines'])
#     # print(len(d['blocks'][i]['lines']))
#     print("---------------------------------")
# # print(d['blocks'][2]['lines'][0]['spans'][0]['size'])
# print(d['blocks'][2]['lines'][0]['spans'][0]['text'])

import fitz
import re


doc = fitz.open('E:/项目/试运行/201808/需求4/处理完成/测试/20180801-申万宏源-风电行业深度报告之海上风电：快马加鞭的海上风电.pdf')
page=doc.loadPage(8)
title = r'^(?!(([图表]+\s*[表]*)*\s*\d+))(.*?)(\.{2,})(\s*\d+)'
# title = r'(^[^\.]*)(\.{2,})(\s*\d+)'
pattern = re.compile(title,re.M)
temp_list = pattern.findall(page.getText())
for i in page.getTextWords():
    print(i)
print(page.getText())
print(temp_list)
doc.close()
# d = page.getText("dict")
# size1_max = 0.0
# result1 = []
# for i in range(len(d['blocks'])):
#     length = len(d['blocks'][i])
#     if d['blocks'][i].__contains__('lines'):
#         length1 = len(d['blocks'][i]['lines'])
#         size_max = 0.0
#         result = []
#         for j in range(length1):
#             if d['blocks'][i]['lines'][j].__contains__('spans'):
#                 size = d['blocks'][i]['lines'][j]['spans'][0]['size']
#                 text = d['blocks'][i]['lines'][j]['spans'][0]['text']
#                 if size == size_max:
#                     result.append(text)
#                 if size > size_max:
#                     size_max = size
#                     result.clear()
#                     result.append(text)
#         if size1_max < size_max:
#             size1_max = size_max
#             result1.clear()
#             result1.append(result)
#         if size1_max == size_max:
#             result1.append(result)
# print(size1_max, '', result1)