from flask import Flask ,render_template,request
from flask import jsonify
import xlrd
import jieba
import jieba.analyse
from gensim import corpora, models, similarities
import codecs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text', methods=['POST','GET'])  # 路由
def text():

#获取前端传过来的值
         name = request.form.get('name','')#这种方式可以获取前端传过来的数据
         #print(name)   #查看赋值是否成功

#数据匹配内容

         # 停用词
         stopwords = []
         stopword_filepath = "stopword.txt"

         # 提取停用词
         file_obj = codecs.open(stopword_filepath, 'r', 'utf-8')
         while True:
             line = file_obj.readline()
             line = line.strip('\r\n')
             if not line:
                 break
             stopwords.append(line)
         file_obj.close()

         # 分词去停用词
         def Fenci(sentence):
             seg_list = jieba.lcut_for_search(sentence, HMM=False)
             results = []
             for seg in seg_list:
                 if seg in stopwords:
                     continue
                 results.append(seg)
             return results

         # 读取excel文件
         df = xlrd.open_workbook('服务外包.xls')
         sheet = df.sheet_by_name("Sheet1")
         rows_num = sheet.nrows

         # 建立文本集
         texts = []
         for i in range(1, rows_num):
             k = sheet.cell_value(i, 1)
             texts.append(k)

         #形成分词列表集
         part_texts = [Fenci(text) for text in texts]

         # 生成字典和语料
         dictionary = corpora.Dictionary(part_texts)
         feature_cnt = len(dictionary.token2id)
         corpus = [dictionary.doc2bow(text) for text in part_texts]

         # 转换Lsi模型
         Lsi = models.LsiModel(corpus)
         index = similarities.SparseMatrixSimilarity(Lsi[corpus], num_features=feature_cnt)  # 矩阵

         # 客户问依次输入
         maxn = 0.0
         idex = -1
         k2 = name
         kw_vector = dictionary.doc2bow(Fenci(k2))
         sim = index[Lsi[kw_vector]]
         for i in range(len(sim)):
             if maxn < sim[i]:
                 maxn = sim[i]
                 idex = i + 1

         if idex == -1:
             name2='亲，未匹配到相应信息，实在抱歉'
         else :
             name2 = sheet.cell_value(idex, 1)#返回匹配得到的值到前端

          #print(name2)  #查看是否获值成功

         return jsonify(result = name2)

if __name__ == '__main__':
    app.run()
