from kubernetes.client import api_client, V1Namespace, V1ObjectMeta, V1NamespaceList
from kubernetes.client.api import core_v1_api
from kubernetes import client, config
from utils import k8s_yaml_helper

# from utils.kubernetes_extensions import CoreAppApiV1


# import yaml
# yaml.load('D:\\k8s-dev\\config01')

# class LoginController():
#     def __int__(self,username,userpasswd):
#         self.username=username
#         self.userpasswd=userpasswd
#     def login(self,user,pwd):
#         if self.username==user & self.userpasswd==pwd:
#             return 1
#         else:
#             return 0
#
#     def get_role(self,user,pwd):
#         if self.login(user,pwd)==1:
#             role=""
#             return role


# class CloudController():
#     def __int__(self,config_file,context):
#         self.config_file=config_file
#         self.context=context

# def choose_config_file(self,loginName):
#     if loginName=="admin":
#         config.load_kube_config(self.config_file,"kubernetes-admin@cluster.local")
#     else:
#         try:
#             config.load_kube_config(self.config_file,loginName)
#         except:
#             print("no context")


#
# mycloud=CloudController()
# mycloud.config_file="D:\\k8s-dev\\config01"
# mycloud.choose_config_file("admin")

#
# config.load_kube_config('D:\\k8s-dev\\compay_config', context="kubernetes-admin@cluster.local")
# v1 = client.CoreV1Api()
# # x=v1.list_pod_for_all_namespaces().items
# #
# # for str in x:
# #     print(str.metadata.name,str.status.phase)
#
#
# # str=v1.list_namespaced_service_account("kube-system")
# # print(str)from utils import k8s_yaml_helper
# #
# # a=v1.list_namespaced_service_account("test")
# # print(a)
# #
#
# # rbac=client.RbacAuthorizationV1Api()
# #
# # body=k8s_yaml_helper.kuberntes_role("test","myrole2",["*"],["pod"],["get", "watch", "list", "create", "update", "patch", "delete"])
# #
# #
# #
# # rbac.create_namespaced_role(namespace="test",body=body)
body = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "nginx-1",
        "labels": {
            "app": "nginx-1"
        }
    },
    "spec": {
        "replicas": 1,
        "template": {
            "metadata": {
                "name": "nginx-2",
                "labels": {
                    "app": "nginx-2"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx:1.15",
                        "resources":{
                            "limits":{
                                "cpu": "50m",
                                "memory": "10Mi",
                            },
                        },
                        "imagePullPolicy": "IfNotPresent"
                    }
                ],
                "restartPolicy": "Always",
            }
        },
        "selector": {
            "matchLabels": {
                "app": "nginx-2"
            },
        }
    }
}
client.AppsV1Api().create_namespaced_deployment(namespace="default",body=body)

# def get_namespace():
#     json = {"namespaces": [], "total": 0}
#     num = 0
#     for ns in v1.list_namespace().items:
#         json["namespaces"].append(
#             {"name": ns.metadata.name,
#              "status": ns.status.phase,
#              "create_time": ns.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")})
#         num = num + 1
#     json["total"] = num
#     return json
#
#
# def get_namespace_by_name(name):
#     json = {"namespaces": [], "total": 0}
#     num = 0
#     # json_item=[x for x in v1.list_namespace().items if x.metadata.name == name]
#     for ns in v1.list_namespace().items:
#         if ns.metadata.name == name:
#             json["namespaces"].append(
#                 {"name": ns.metadata.name,
#                  "status": ns.status.phase,
#                  "create_time": ns.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")})
#             num = num + 1
#     json["total"] = num
#     return json
#
#
# def check_namespace_exists(name):
#     is_exist = False
#     json_item = [x for x in v1.list_namespace().items if x.metadata.name == name]
#     if len(json_item) > 0:
#         is_exist = True
#     else:
#         is_exist = False
#     return is_exist
#
#
# def create_namespace(name):
#     body = {
#         "apiVersion": "v1",
#         "kind": "Namespace",
#         "metadata": {
#             "name": name, }
#     }
#     v1.create_namespace(body=body, async_req=True)
#
#
# def get_all_pod_infos():
#     pod_list = {"pods": [], "total": 0}
#     num = 0
#     reg_list = v1.list_pod_for_all_namespaces().items
#     for pod in reg_list:
#         pod_list["pods"].append(
#             {
#                 "name": pod.metadata.name,
#                 "namespace": pod.metadata.namespace,
#                 "status": pod.status.phase,
#                 "node_name": pod.spec.node_name,
#                 "node_ip": pod.status.host_ip,
#                 "pod_ip": pod.status.pod_ip,
#                 "start_time": pod.status.start_time.strftime("%Y-%m-%d %H:%M:%S")
#             }
#         )
#         num = num + 1
#     pod_list["total"] = num
#     return pod_list
#
#
# def get_node_infos():
#     node_list = {"node": [], "total": 0}
#     num = 0
#     reg_list = v1.list_node().items
#     for node in reg_list:
#         node_address = ""
#         for address in node.status.addresses:
#             if address.type == "InternalIP":
#                 node_address = address.address
#         node_list["node"].append(
#             {
#                 "name": node.metadata.name,
#                 "address": node_address,
#                 "os": node.status.node_info.os_image,
#                 "docker_version": node.status.node_info.container_runtime_version,
#                 "kubelet_version": node.status.node_info.kubelet_version
#             }
#         )
#         num = num + 1
#     node_list["total"] = num
#     return node_list
#
#
# def get_images_infos():
#     images_list = {"images": [], "total": 0, "node_list": []}
#     reg_list = v1.list_node().items
#     num = 0
#     for node in reg_list:
#         node_name = node.metadata.name
#         if node_name not in images_list["node_list"]:
#             images_list["node_list"].append(node_name)
#         for img in node.status.images:
#             for name in img.names:
#                 if "sha256" not in str(name):
#                     size = img.size_bytes
#                     print(name)
#                     if str(name) == None or str(name) == "" or name == "<none>@<none>":
#                         images_list["images"].append(
#                             {
#                                 "node_name": node_name,
#                                 "name": str(name).split('@')[0],  # "version":version,
#                                 "version": str(name).split('@')[1],
#                                 "size": size
#
#                             })
#                         num = num + 1
#                     else:
#                         images_list["images"].append(
#                             {
#                                 "node_name": node_name,
#                                 "name": str(name).split(':')[0],  # "version":version,
#                                 "version": str(name).split(':')[1],
#                                 "size": size
#
#                             })
#                         num = num + 1
#     images_list['total'] = num
#     return images_list
#
#
# def get_imgaes_by_arg(node_name, name):
#     list = get_images_infos()
#     search_list = {"images": [], "total": 0, "node_list": []}
#     search_list["node_list"] = list["node_list"]
#     num = 0
#     for img in list["images"]:
#         if name == None or name == "":
#             if img["node_name"] == node_name:
#                 search_list["images"].append(img)
#                 num = num + 1
#         else:
#             if img["node_name"] == node_name and img["name"] == name:
#                 search_list["images"].append(img)
#                 num = num + 1
#     search_list["total"] = num
#     return search_list
#
#
# def get_apps():
#     result = {"apps": [], "total": 0}
#     num = 0
#     list = []
#     for deploy in v1.list_deployment_for_all_namespaces().items:
#         state = "Error"
#         if deploy.status.replicas == deploy.status.ready_replicas:
#             state = "Running"
#         list.append(
#             {
#                 "name": deploy.metadata.name,
#                 "namespace": deploy.metadata.namespace,
#                 "images": deploy.spec.template.spec.containers[0].image,
#                 "replicas": deploy.status.replicas,
#                 "ready_replicas": deploy.status.ready_replicas,
#                 "status": state,
#                 "sourcetype": "Deployment"
#             }
#         )
#         num = num + 1
#     for daemonset in v1.list_daemonsets_for_all_namespaces().items:
#         state = "Error"
#         if daemonset.status.current_number_scheduled == daemonset.status.number_ready:
#             state = "Running"
#         list.append(
#             {
#                 "name": daemonset.metadata.name,
#                 "namespace": daemonset.metadata.namespace,
#                 "images": daemonset.spec.template.spec.containers[0].image,
#                 "replicas": daemonset.status.current_number_scheduled,
#                 "ready_replicas": daemonset.status.number_ready,
#                 "status": state,
#                 "sourcetype": "DaemonSet"
#             }
#         )
#         num = num + 1
#     for statefulset in v1.list_statefulset_for_all_namespaces().items:
#         state = "Error"
#         if statefulset.status.replicas == statefulset.status.ready_replicas:
#             state = "Running"
#         list.append(
#             {
#                 "name": statefulset.metadata.name,
#                 "namespace": statefulset.metadata.namespace,
#                 "images": statefulset.spec.template.spec.containers[0].image,
#                 "replicas": statefulset.status.replicas,
#                 "ready_replicas": statefulset.status.ready_replicas,
#                 "status": state,
#                 "sourcetype": "statefulset"
#             }
#         )
#         num = num + 1
#     result["apps"] = list
#     result["total"] = num
#     return result
#
#
# def get_all_service():
#     result = {"service": [], "total": 0}
#     v1.list_service_for_all_namespaces()
