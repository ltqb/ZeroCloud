from flask import Flask, jsonify, request

from utils import mysql_helper
from controller import db_controller, kubernetes_controller, ansible_helper

# import urllib
from utils.k8s_yaml_helper import kubernetes_deployment

app = Flask(__name__)

import toml


# kubernetes_controller.current_config = kubernetes_controller.get_config_name()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ns')
def namespace():
    common = kubernetes_controller.V1_Controller()
    namespaces = common.get_namespace()
    return jsonify(namespaces)


@app.route('/ns/<name>', methods=["GET", "POST"])
def namespace_by_name(name):
    common = kubernetes_controller.V1_Controller()
    if request.method == "GET":
        if name != "":
            namespaces = common.get_namespace_by_name(name=name)
            return jsonify(namespaces)
    else:
        if request.method == "POST":
            new_name = request.form.get('name')
            print(new_name)
            print(common.check_namespace_exists(new_name))
            if common.check_namespace_exists(new_name) == False:
                common.create_namespace(new_name)
                result = {"op": "add", "result": 1}
                return jsonify(result)
            else:
                result = {"op": "add", "result": 0}
                return jsonify(result)

        else:
            return jsonify({"method": "other"})


@app.route('/ns/del/<name>', methods=["POST", ])
def namespace_delete(name):
    common = kubernetes_controller.V1_Controller()
    result = {}
    if request.method == "POST":
        data = request.form.get('name')
        print(data)
        bool_exists = common.check_namespace_exists(data)
        if bool_exists == True:
            state = common.v1.delete_namespace(data, async_req=True)
            print(state)
            result = {"op": "delete", "result": 1}
        else:
            result = {"op": "delete", "result": 0}

    return jsonify(result)


@app.route('/pods')
def get_all_pods():
    common = kubernetes_controller.V1_Controller()
    all_pods = common.get_all_pod_infos()
    return jsonify(all_pods)


@app.route('/configfiles')
def get_config_files():
    config_json = toml.load("config.toml")
    result = {}
    config_list = []
    for myconifg in config_json["clusters"]:
        print(myconifg)
        config_list.append({
            "config_name": myconifg,
            "config_path": config_json["clusters"][myconifg]["config_path"]
        })
    result = {"total": len(config_list), "hostinfo": config_list}
    return jsonify(result)


@app.route('/chooseConfig', methods=["POST", ])
def choose_config_files():
    result = {}
    if request.method == "POST":
        name = request.form.get('name')
        print(name)
        kubernetes_controller.load_config()
        result = kubernetes_controller.write_current_name(name)
    return jsonify(result)


@app.route('/nodeinfos')
def get_node_infos():
    # kubernetes_controller.write_current_name()
    node_infos = kubernetes_controller.ClusterStatus_Controller.all_nodes
    result = {"total": len(node_infos), "nodeinfos": node_infos}
    return jsonify(result)


@app.route('/images')
def get_all_images():
    common = kubernetes_controller.V1_Controller()
    all_images = common.get_images_infos()
    return jsonify(all_images)


@app.route('/images/filter', methods=["POST", ])
def search_images():
    result = {}
    common = kubernetes_controller.V1_Controller()
    if request.method == "POST":
        node_name = request.form.get('nodename')
        name = request.form.get('name')
        result = common.get_imgaes_by_arg(node_name, name)
    print(result)
    return jsonify(result)


from controller import ansible_helper


@app.route('/dbdev')
def insert_dev_state():
    facts = ansible_helper.get_all_host_fact()
    result = ansible_helper.write_host_state_2_db(facts)
    return jsonify(result)


# @app.route('/images/download/status', methods=["POST"])
# def get_bar_images():
#     bar = {}
#     if request.method == "POST":
#         tarname = request.form.get('tar_name')
#         if ansible_helper.list["name"] == tarname:
#             percent = max(ansible_helper.list["percent"])
#             bar = {"name": tarname, "percent": percent}
#         else:
#             bar = {"name": tarname, "percent": 0}
#     return jsonify(bar)
#
#
# @app.route('/images/download/start', methods=["POST"])
# def start_download():
#     result = {"image_name": "", "status": False, "thead": None}
#     if request.method == "POST":
#         node_name = request.form.get('node_name')
#         name = request.form.get('name')
#         save_path = request.form.get('save_path')
#         tarname = request.form.get('tar_name')
#         t = threading.Thread(target=ansible_helper.docker_images_download,
#                              args=(node_name, name, "/tmp/" + tarname, tarname))
#         t.start()
#         result = {"image_name": name, "status": t.isAlive(), "thead": t.ident}
#     return jsonify(result)


# @app.route('/containers')
# def get_containers():
#     url = "http://212.64.85.14:5000/v1/api/containers/"
#     req = urllib.request.urlopen(url)
#     a = json.load(req)
#     return jsonify(a)


# @app.route('/container/remove', methods=["POST"])
# def remove_container():
#     url = "http://212.64.85.14:5000/v1/api/container/remove"
#     if request.method == "POST":
#         result = requests.post(url, request.form)
#     return jsonify(result)


@app.route('/apps')
def get_apps():
    common = kubernetes_controller.V1_Controller()
    result = common.get_apps()
    return jsonify(result)


@app.route('/alldeviceinfo')
def get_devices():
    common = kubernetes_controller.V1_Controller()
    all_pods = common.get_all_pod_infos()
    all_devices = mysql_helper.get_all_device_to_list()
    all_devices["podTotal"] = all_pods["total"]
    return jsonify(all_devices)


@app.route('/login_auth', methods=["POST"])
def auth_login():
    result = {"username": "", "result": False}
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        auth_result = db_controller.auth_user_info(user_name=name, user_pwd=password)
        result = {"username": name, "result": auth_result["auth_state"], "menu": auth_result["menu_role"]}
    return jsonify(result)


@app.route('/cloudStatus')
def get_cloud_status():
    my_status = kubernetes_controller.ClusterStatus_Controller()
    config_path, common_prom = kubernetes_controller.load_config()
    context = "kubernetes-admin@cluster.local"
    kubernetes_controller.config.load_kube_config(config_path, context=context)
    api = kubernetes_controller.client.CoreV1Api()
    my_status.prom_url = common_prom
    my_status.all_nodes = api.list_node().items
    my_status.all_pods = api.list_pod_for_all_namespaces().items
    my_status.all_services = api.list_service_for_all_namespaces().items
    result = my_status.get_cluster_status()
    return jsonify(result)


@app.route('/hostsInfos', methods=["POST", "GET", ])
def get_all_hosts():
    db_data = db_controller.get_all_hosts_info()
    hostsinfo = []
    for row in db_data:
        dev_type = row.device_type
        # dev_name = ""
        # if dev_type == 0:
        #     dev_name = "虚拟机"
        # elif dev_type == 1:
        #     dev_name = "物理机"
        # else:
        #     dev_name = "未知"
        hostsinfo.append({
            "name": row.name,
            "user_name": row.user_name,
            "user_password": row.user_password,
            "ip_address": row.ip_address,
            "ssh_port": row.ssh_port,
            "device_type": dev_type,
            "location": row.location,
            "remark": row.remark,
            "create_time": row.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": row.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "device_status": row.device_status,
            "own_cluster": row.own_cluster

        })
    result = {"total": len(hostsinfo), "hostinfo": hostsinfo}
    return jsonify(result)


@app.route('/addhost', methods=["POST", ])
def insert_host():
    result = {}
    if request.method == "POST":
        name = request.form.get('name')
        ip_address = request.form.get('ip_address')
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        ssh_port = request.form.get('ssh_port')
        device_type = request.form.get('machine_type')
        location = request.form.get('location')
        remark = ""
        own_cluster = request.form.get('cluster')
        result = db_controller.add_host_info(name, ip_address, user_name, user_password, int(ssh_port), device_type,
                                             location,
                                             remark, own_cluster)
    return jsonify(result)


@app.route('/deleleHost', methods=["POST", ])
def delete_host():
    result = {}
    if request.method == "POST":
        name = request.form.get('name')
        result = db_controller.delete_host_info(name)
    return jsonify(result)


@app.route('/app/add', methods=["POST", ])
def deploy_add():
    result = {}
    if request.method == "POST":
        app_controller = request.form.get('controller')
        if app_controller == "Deployment":
            name = request.form.get('name')
            replicas = request.form.get('replicas')
            namespace = request.form.get('namespace')
            image = request.form.get('image')
            cpu = request.form.get('cpu')
            memory = request.form.get('memory')
            deploy_json = {
                "name": name,
                "replicas": int(replicas),
                "image": image,
                "cpu": cpu,
                "memory": memory + 'Mi'
            }
            my_con = kubernetes_controller.AppControllor()
            my_con.namespace = namespace
            my_con.body = kubernetes_deployment(deploy_json)
            my_con.create_deploy_app()
            result = {
                "name": name,
                "controller": "deployment",
                "oper": "create",
                "result": "success"
            }
            print(result)
    return jsonify(result)


@app.route('/app/del', methods=["POST", ])
def deploy_del():
    result = {}
    if request.method == "POST":
        app_controller = request.form.get('controller')
        if app_controller == "Deployment":
            name = request.form.get('name')
            namespace = request.form.get('namespace')
            my_con = kubernetes_controller.AppControllor()
            my_con.namespace = namespace
            my_con.delete_deploy_app(name)
            result = {
                "name": name,
                "controller": "deployment",
                "oper": "delete",
                "result": "success"
            }
            print(result)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
