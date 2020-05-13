import json
import threading

from flask import Flask, jsonify, abort, request, Request
from utils import common, ansible_helper, mysql_helper

import urllib

from utils.mysql_helper import DeviceView

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ns')
def namespace():
    namespaces=common.get_namespace()
    return jsonify(namespaces)

@app.route('/ns/<name>',methods=["GET","POST"])
def namespace_by_name(name):
    if request.method=="GET":
        if name!="":
            namespaces=common.get_namespace_by_name(name=name)
            return jsonify(namespaces)
    else:
         if request.method=="POST":
             new_name=request.form.get('name')
             print(new_name)
             print(common.check_namespace_exists(new_name))
             if common.check_namespace_exists(new_name)==False:
                 common.create_namespace(new_name)
                 result = {"op":"add","result":1}
                 return jsonify(result)
             else:
                 result = {"op":"add","result":0}
                 return jsonify(result)

         else:
             return jsonify({"method":"other"})

@app.route('/ns/del/<name>',methods=["POST",])
def namespace_delete(name):
    result={}
    if request.method == "POST":
        data=request.form.get('name')
        print(data)
        bool_exists=common.check_namespace_exists(data)
        if bool_exists ==True:
           common.v1.delete_namespace(data,async_req=True)
           result = {"op":"delete","result":1}
        else:
           result = {"op":"delete","result":0}

    return jsonify(result)



@app.route('/pods')
def get_all_pods():
    all_pods=common.get_all_pod_infos()
    return jsonify(all_pods)

@app.route('/images')
def get_all_images():
    all_images=common.get_images_infos()
    return jsonify(all_images)

@app.route('/images/filter',methods=["POST",])
def search_images():
    result={}
    if request.method=="POST":
        node_name = request.form.get('nodename')
        name=request.form.get('name')
        result=common.get_imgaes_by_arg(node_name,name)
    print(result)
    return jsonify(result)


@app.route('/images/download/status',methods=["POST"])
def get_bar_images():
    bar={}
    if request.method == "POST":
        tarname = request.form.get('tar_name')
        if ansible_helper.list["name"]==tarname:
            percent=max(ansible_helper.list["percent"])
            bar={"name":tarname,"percent":percent}
        else:
            bar={"name":tarname,"percent":0}
    return jsonify(bar)

@app.route('/images/download/start',methods=["POST"])
def start_download():
    result={"image_name":"","status":False,"thead":None}
    if request.method=="POST":
        node_name=request.form.get('node_name')
        name = request.form.get('name')
        save_path=request.form.get('save_path')
        tarname=request.form.get('tar_name')
        t =threading.Thread(target=ansible_helper.docker_images_download,args=(node_name,name,"/tmp/"+tarname,tarname))
        t.start()
        result={"image_name":name,"status":t.isAlive(),"thead":t.ident}
    return jsonify(result)

@app.route('/containers')
def get_containers():
    url="http://172.16.200.4:5000/v1/api/containers/"
    req=urllib.request.urlopen(url)
    a=json.load(req)
    return jsonify(a)


@app.route('/apps')
def get_apps():
    result=common.get_apps()
    return jsonify(result)


@app.route('/alldeviceinfo')
def get_devices():
    all_pods = common.get_all_pod_infos()
    all_devices=mysql_helper.get_all_device_to_list()
    all_devices["podTotal"]=all_pods["total"]
    return jsonify(all_devices)





if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
