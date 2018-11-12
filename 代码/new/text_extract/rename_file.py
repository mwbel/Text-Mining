import os
import fitz
import re

def rename(path):
    namelist = []
    data = r'[1-9][0-9]{3}.*[0-9]{1,2}.*[0-9]{1,2}'
    regEx = r'\d*'
    broker = r'.{2}'
    for file in os.listdir(path):
        if file[-4:] == ".pdf":
            name = ''
            doc = fitz.open(os.path.join(path, file))
            page_count = doc.pageCount
            page = doc.loadPage(1)
            page_text = page.getText()
            fdata = re.findall(data, page_text)
            deal_data = re.findall(regEx, fdata)
            for i in range(len(deal_data)):
                if i==1 and len(deal_data[i])==1:
                    deal_data[i] = '0'+deal_data[i]
                name = name + deal_data[i]
            for i in range(page_count):
                page = doc.loadPage(i)
                page_text = page.getText()


            




            


