from kubernetes.client import api_client, V1Namespace, V1ObjectMeta
from kubernetes.client.api import core_v1_api
from kubernetes import client ,config


config.load_kube_config('C:\\k8s_172.yaml')
v1 = client.CoreV1Api()

# def create_api_conn_k8s(k8s_url,token):
#     configuration = client.Configuration()
#     configuration.host = k8s_url
#     configuration.verify_ssl = False
#     configuration.api_key = {"authorization": "Bearer " + token}
#     client1 = api_client.ApiClient(configuration=configuration)
#     api = core_v1_api.CoreV1Api(client1)
#     return api

def get_namespace():
    json = {"namespaces": [],"total":0}
    num=0
    for ns in v1.list_namespace().items:
        json["namespaces"].append(
            {"name": ns.metadata.name,
             "status": ns.status.phase,
             "create_time": ns.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")})
        num = num + 1
    json["total"] = num
    return json

def get_namespace_by_name(name):
    json = {"namespaces": [],"total":0}
    num = 0
    #json_item=[x for x in v1.list_namespace().items if x.metadata.name == name]
    for ns in v1.list_namespace().items:
        if ns.metadata.name==name:
           json["namespaces"].append(
               {"name": ns.metadata.name,
                "status": ns.status.phase,
                "create_time": ns.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")})
           num = num + 1
    json["total"] = num
    return json

def check_namespace_exists(name):
    is_exist=False
    json_item = [x for x in v1.list_namespace().items if x.metadata.name == name]
    if len(json_item)>0:
        is_exist=True
    else:
        is_exist=False
    return is_exist

def create_namespace(name):
    body = {
    "apiVersion": "v1",
    "kind": "Namespace",
    "metadata": {
    "name": name,}
    }
    v1.create_namespace(body=body,async_req=True)


def get_all_pod_infos():
    pod_list= {"pods": [], "total": 0}
    num = 0
    reg_list=v1.list_pod_for_all_namespaces().items
    for pod in reg_list:
        pod_list["pods"].append(
            {
                "name":pod.metadata.name,
                "namespace":pod.metadata.namespace,
                "status":pod.status.phase,
                "node_name":pod.spec.node_name,
                "node_ip":pod.status.host_ip,
                "pod_ip":pod.status.pod_ip,
                "start_time":pod.status.start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        num = num + 1
    pod_list["total"]=num
    return pod_list

def get_node_infos():
    node_list={"node":[],"total":0}
    num=0
    reg_list=v1.list_node().items
    for node in reg_list:
        node_address=""
        for address in node.status.addresses:
            if address.type=="InternalIP":
                node_address=address.address
        node_list["node"].append(
            {
                "name":node.metadata.name,
                "address":node_address,
                "os":node.status.node_info.os_image,
                "docker_version":node.status.node_info.container_runtime_version,
                "kubelet_version":node.status.node_info.kubelet_version
            }
        )
        num=num+1
    node_list["total"]=num
    return node_list


def get_images_infos():
    images_list={"images":[],"total":0,"node_list":[]}
    reg_list=v1.list_node().items
    num=0
    for node in reg_list:
        node_name=node.metadata.name
        if node_name not in images_list["node_list"]:
            images_list["node_list"].append(node_name)
        for img in node.status.images:
            for name in img.names:
                if "sha256" not in str(name):
                    size=img.size_bytes
                    images_list["images"].append(
                        {
                            "node_name":node_name,
                            "name":str(name).split(':')[0],#"version":version,
                            "version":str(name).split(':')[1],
                            "size":size

                        })
                    num = num + 1
    images_list['total']=num
    return images_list

def get_imgaes_by_arg(node_name,name):
    list=get_images_infos()
    search_list={"images":[],"total":0,"node_list":[]}
    search_list["node_list"]=list["node_list"]
    num=0
    for img in list["images"]:
        if name==None or name=="":
            if img["node_name"]==node_name:
                search_list["images"].append(img)
                num=num+1
        else:
            if img["node_name"] == node_name and img["name"]==name:
                search_list["images"].append(img)
                num=num+1
    search_list["total"]=num
    return search_list




#print(get_imgaes_by_arg("sjl01","gcr.io/google_containers/pause-amd64"))








#k8s_url="https://192.168.56.104:6443"
#token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWdtZHh4Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJlZmEzMWNjOS04MDg0LTExZWEtODQ0Yy0wODAwMjcyMWQzOGMiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.F2QwOKTAxZI0DDVF1HhPJ-dCiUE2iumPliH-E3ryBwTrWyd428jx6g_k6nTohqo4ncqJqxRQUuZ_PX-Djw3fWgEQUu-46Ivmh27SmBuCFqmibTRytyc2LxYIluAfCJLxFXTQwhENN6_MjydeEhFmTk9ijPaINYeGz2Kj5h5SufEd3JsMHnSohm3E-sJdkHStCllfD9hKdeGJJa2yABcRkY1nKjgQEYmrAyZiBccKzCBffN3Pnqvto2BQu44mDqPXPyUYa_ygbvJFekWgDTJIiosqBZAJghXN6MNI6tG_VEanzv74B9RcrlVa4O9Gzciw4Ec2JuVy_yLnygiLhWJMDQ"

# api=create_api_conn_k8s(k8s_url,token)
# list=api.list_namespace().items
#
# t=V1Namespace.status
# t2=V1ObjectMeta
# t3=datetime.datetime

#print(list)
#for item in list:
#    print(item.metadata.name,":",item.metadata.creation_timestamp)
#
# list2=api.list_node().items
#
# list3=api.list_pod_for_all_namespaces().items
# for item in list3:
#     print(item.metadata.name,"|",item.status.host_ip,"|",item.status.pod_ip)



