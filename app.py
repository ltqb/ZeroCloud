from flask import Flask,jsonify, abort, request
from utils import common
import json

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

if __name__ == '__main__':
    app.run()
