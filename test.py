from flask import Flask ,render_template,abort,request
from flask import jsonify,json
import json
import urllib.request
import xlrd
import jieba
import jieba.analyse
from gensim import corpora, models, similarities
import codecs
# 读取excel文件
df = xlrd.open_workbook('服务外包.xls')
sheet = df.sheet_by_name("Sheet1")
rows_num = sheet.nrows

# 建立文本集
texts = []
for i in range(1, rows_num):
    k = sheet.cell_value(i, 1)
    texts.append(k)

print(texts)