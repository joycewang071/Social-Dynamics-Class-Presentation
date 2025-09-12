import sys
import importlib
importlib.reload(sys)
import re
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfpage import PDFTextExtractionNotAllowed

# 对本地保存的pdf文件进行读取和写入到txt文件当中


# 定义解析函数
def pdftotxt(path,new_name):
    # 创建一个文档分析器
    parser = PDFParser(path)
    # 创建一个PDF文档对象存储文档结构
    document =PDFDocument(parser)
    # 判断文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储资源
        resmag =PDFResourceManager()
        # 设定参数进行分析
        laparams =LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(resmag)
        device =PDFPageAggregator(resmag,laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(resmag, device)
        # 处理每一页
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout =device.get_result()
            for y in layout:
                if(isinstance(y,LTTextBoxHorizontal)):
                    with open("C:/Users/10292/Downloads/news_txt/%s"%(new_name),'a',encoding="utf-8") as f:
                        f.write(re.sub('[^\u4e00-\u9fa5]+', '', y.get_text())+"\n")

############ 还是要用‘’来替换， 而不是‘ ’， 否则会出现不必要的分割

## From PDF to TXT
i=0
f_list = os.listdir('C:/Users/10292/Downloads/news')
for f in f_list:
    f1_list = os.listdir(f"C:/Users/10292/Downloads/news/{f}")
    for f1 in f1_list:
        f2_list = os.listdir(f"C:/Users/10292/Downloads/news/{f}/{f1}")
        for f2 in f2_list:
            path =open( f"C:/Users/10292/Downloads/news/{f}/{f1}/{f2}",'rb')
            pdftotxt(path,f"{f1}__{f2[:-4]}.txt")
            i=i+1
            print(i,path)
    

