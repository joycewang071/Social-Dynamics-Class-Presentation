"""
Script: PDF to TXT batch extractor for Chinese text
Author: Xinxin Wang

"""

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

# Read locally saved PDF files and write extracted text into TXT files


# Define parsing function
def pdftotxt(path,new_name):
    # Create a document parser
    parser = PDFParser(path)
    # Create a PDF document object to store the document structure
    document =PDFDocument(parser)
    # Check whether the file allows text extraction
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # Create a PDF resource manager to store shared resources
        resmag =PDFResourceManager()
        # Set layout analysis parameters
        laparams =LAParams()
        # Create a PDF device
        # device = PDFDevice(resmag)
        device =PDFPageAggregator(resmag,laparams=laparams)
        # Create a PDF interpreter
        interpreter = PDFPageInterpreter(resmag, device)
        # Process each page
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # Receive the LTPage object of the current page
            layout =device.get_result()
            for y in layout:
                if(isinstance(y,LTTextBoxHorizontal)):
                    with open("C:/Users/10292/Downloads/news_txt/%s"%(new_name),'a',encoding="utf-8") as f:
                        f.write(re.sub('[^\u4e00-\u9fa5]+', '', y.get_text())+"\n")

############ Use '' (empty string) for replacement instead of a single space ' ' to avoid unnecessary splits

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
    

