from flask import Flask,render_template
app = Flask(__name__)
fpath = 'E:\\codee\\visualization\static\json'
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.visual_data_system
def GetJfile(fpath):      #读取json数据并做处理
    import os
    import json
    jlist,namelist,dbdata = [],[],[]
    jlist = os.listdir(fpath)      #读取给定路径下的所有文件
    for i in range(len(jlist)):      #循环遍历文件
        filepath = os.path.join(fpath,jlist[i])   #补全文件路径
        name,extend = os.path.splitext(jlist[i])       #将文件的名字和扩展名拆开
        namelist.append(name)      #将文件名存入namelist用于创建数据库中对应的集合
        if os.path.isfile(filepath):    #判断是否是文件
            jfile = open(filepath)   #打开文件
            jdata = json.load(jfile)    #处理json文件
            dbdata.append(jdata)    #将处理后的json文件内容添加到列表中
    return namelist,dbdata

def GetData():

    namelist, dbdata = GetJfile(fpath)
    alldata = {}
    for i in namelist:        #循环遍历数据库中各个集合的数据，并存入到一个字典中
        for j in db[i].find({},{'_id':0}):
            alldata = dict(alldata,**j)
    return alldata

def InsertDB():      #插入数据


    namelist, dbdata = GetJfile(fpath)
    for i in range(len(namelist)):        #循环创建集合并向集合内插入数据
        db[namelist[i]].insert(dbdata[i])

def GetLddata():
    alldata = GetData()
    city = []
    for i in alldata['area']:        #循环读取‘area’对应城市名数据
        citydic = dict(text=i,max=450)    #创建字典
        city.append(citydic)   #添加到city列表用用于雷达图
    return city

@app.route('/_break')
def _break():
    alldata = GetData()      # 调用GetData函数 获取包含数据四个集合中的所有内容，用于向前端data传值
    return render_template('break.html', data=alldata)
@app.route('/_china')
def _china():
    alldata = GetData()
    return render_template('china.html', data=alldata)
@app.route('/_trend')
def _trend():
    alldata = GetData()
    return render_template('trend.html', data=alldata)
@app.route('/_type')
def _type():
    alldata = GetData()
    return render_template('type.html', data=alldata)
@app.route('/')
def all():
    alldata = GetData()
    city = GetLddata()    #调用GetLddata()函数，获得city列表，向前端textlist传值
    return render_template('index.html', data = alldata,textlist = city)
@app.route('/_leida')
def leida():
    alldata = GetData()
    city = GetLddata()
    return render_template('leida.html', data=alldata,textlist = city)

if __name__ == '__main__':
    # InsertDB()
    app.run(host = '0.0.0.0')   #服务器ip地址 192.168.34.46:5000

