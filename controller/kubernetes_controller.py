import datetime
from kubernetes import client, config

from controller.kubernetes_extensions import CoreAppApiV1
from utils import k8s_yaml_helper
from controller import os_controller, db_controller

import toml


def get_config_name():
    file_a = "/opt/config.toml"
    cluster_config = toml.load(file_a)
    return cluster_config["current_cluster"]["name"]


def write_current_name(current_name):
    file_a = "/opt/config.toml"
    cluster_config = toml.load(file_a)
    cluster_config["current_cluster"]["name"] = current_name
    with open(r"/opt/config.toml", 'w') as f:
        r = toml.dump(cluster_config, f)
    return r


def load_config():
    file_a = r"/opt/config.toml"
    # file_a = "/opt/config.toml"
    cluster_config = toml.load(file_a)
    # cluster_config["current_cluster"] = current_cluster
    # cluster_name = cluster_config[current_cluster]["name"]
    cluster = cluster_config["clusters"][get_config_name()]
    config_path = cluster["config_path"]
    common_prom = cluster["prom_url"]
    # print(config_path, common_prom)
    return config_path, common_prom


def load_current_config():
    config_path, common_prom = load_config()
    context = "kubernetes-admin@cluster.local"
    config.load_kube_config(config_path, context=context)
    v1 = client.CoreV1Api()
    extenapi = client.AppsV1Api()
    return v1, extenapi


def check_k8s_config(func):
    config_path, common_prom = load_config()
    context = "kubernetes-admin@cluster.local"
    config.load_kube_config(config_path, context=context)
    return func


# config_path, common_prom = load_config()
# context = "kubernetes-admin@cluster.local"
# config.load_kube_config(config_path, context=context)

# config.load_kube_config('D:\\k8s-dev\\compay_config', context="kubernetes-admin@cluster.local")

from utils import prometheus_connect


class ClusterStatus_Controller():
    config_path, common_prom = load_config()
    context = "kubernetes-admin@cluster.local"
    config.load_kube_config(config_path, context=context)
    api = client.CoreV1Api()
    prom_url = common_prom
    all_nodes = api.list_node().items
    all_pods = api.list_pod_for_all_namespaces().items
    all_services = api.list_service_for_all_namespaces().items

    # def refresh_config(self):
    #     config_path, common_prom = load_config()
    #     context = "kubernetes-admin@cluster.local"
    #     config.load_kube_config(config_path, context=context)
    #     global api, prom_url, all_nodes, all_pods, all_services
    #     api = client.CoreV1Api()
    #     prom_url = common_prom
    #     all_nodes = api.list_node().items
    #     all_pods = api.list_pod_for_all_namespaces().items
    #     all_services = api.list_service_for_all_namespaces().items
    #     return api, prom_url, all_nodes, all_pods, all_services

    def get_cpu_request_total(self):
        my_prom = prometheus_connect.PrometheusConnect()
        my_prom.url = self.prom_url
        cpu_metrics = my_prom.get_current_metric_value("kube_pod_container_resource_requests_cpu_cores")
        cpu_reuqest = 0.0
        for metric in cpu_metrics:
            v_cpu = metric["value"][1]
            cpu_reuqest = cpu_reuqest + float(v_cpu)
        return round(cpu_reuqest * 1000, 2)

    def get_mem_request_total(self):
        my_prom = prometheus_connect.PrometheusConnect()
        my_prom.url = self.prom_url
        mem_metrics = my_prom.get_current_metric_value("kube_pod_container_resource_requests_memory_bytes")
        mem_request = 0
        for metric in mem_metrics:
            v_mem = metric["value"][1]
            # print(v_mem)
            mem_request = mem_request + int(v_mem)
        return round(float(mem_request) / 1024, 2)

    def get_commpent_stauts(self):
        # all_pods = self.api.list_pod_for_all_namespaces().items
        api_server_running = 0
        api_server_not = 0
        controller_manager_running = 0
        controller_manager_not = 0
        scheduler_running = 0
        scheduler_not = 0
        proxy_running = 0
        proxy_not = 0
        # etcd_running = 0
        # etcd_not = 0

        for item in self.all_pods:
            pod_name = item.metadata.name
            pod_state = item.status.phase
            if "kube-apiserver" in pod_name:
                api_server_not = api_server_not + 1
                if pod_state == "Running":
                    api_server_running = api_server_running + 1

            if "kube-controller-manager" in pod_name:
                controller_manager_not = controller_manager_not + 1
                if pod_state == "Running":
                    controller_manager_running = controller_manager_running + 1

            if "kube-scheduler" in pod_name:
                scheduler_not = scheduler_not + 1
                if pod_state == "Running":
                    scheduler_running = scheduler_running + 1

            if "kube-proxy" in pod_name:
                proxy_not = proxy_not + 1
                if pod_state == "Running":
                    proxy_running = proxy_running + 1

        return {
            "api_server": str(api_server_running) + " / " + str(api_server_not),
            "controller-manager": str(controller_manager_running) + " / " + str(controller_manager_not),
            "scheduler": str(scheduler_running) + " / " + str(scheduler_not),
            "proxy": str(proxy_running) + " / " + str(proxy_not),
            "kubelet": str(proxy_running) + " / " + str(proxy_not),
            "etcd": "1 / 1"
        }

    def get_cluster_status(self):
        # all_nodes = self.api.list_node().items
        # all_pods = self.api.list_pod_for_all_namespaces().items
        # all_services = self.api.list_service_for_all_namespaces().items
        node_total = len(self.all_nodes)
        pod_total = len(self.all_pods)
        service_total = len(self.all_services)
        cpu_total = 0
        mem_total = 0
        for node in self.all_nodes:
            node_cpu = node.status.allocatable["cpu"]
            node_mem = node.status.allocatable["memory"]
            if 'm' in node_cpu:
                a = str(node_cpu).split('m')[0]
                cpu_total = int(a) + cpu_total
            else:
                cpu_total = int(a) * 1000 + cpu_total

            if 'Ki' in node_mem:
                b = str(node_mem).split('Ki')[0]
                mem_total = int(b) + mem_total
            else:
                mem_total = int(a) + mem_total
        # print(cpu_total, mem_total)
        node_infos = self.all_nodes[0].status.node_info
        containner_runtime_version = node_infos.container_runtime_version
        runtime = str(containner_runtime_version).split(":")[0]
        runtime_version = str(containner_runtime_version).split("/")[-1]
        operating_system = node_infos.operating_system
        os_image = node_infos.os_image
        kernel_version = node_infos.kernel_version
        creation_timestamp = self.all_nodes[0].metadata.creation_timestamp
        k8s_version = node_infos.kubelet_version
        cpu_use_total = self.get_cpu_request_total()
        mem_use_total = self.get_mem_request_total()
        commpent = self.get_commpent_stauts()
        # print(runtime, runtime_version, operating_system, os_image, kernel_version, creation_timestamp, k8s_version)
        return {
            "envinfo": {
                'runtime': runtime,
                'version': runtime_version,
                'operating_system': operating_system,
                'os_image': os_image,
                'kernel_version': kernel_version,
                "creation_timestamp": creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "k8sinfo": {
                "manager": "Kubernetes",
                "creation_timestamp": creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "cloud_type": "Private Cloud",
                "version": k8s_version,
                "cpu_total": round(cpu_total, 2),
                "cpu_request": cpu_use_total,
                "cpu_usage": round(float(cpu_use_total) / float(cpu_total) * 100, 2),
                "mem_total": round(mem_total / 1024, 2),
                "mem_request": round(mem_use_total / 1024, 2),
                "mem_usage": round(float(mem_use_total) / float(mem_total) * 100, 2),
                "mem_free": round(round(mem_total / 1024, 2) - round(mem_use_total / 1024, 2), 2),
                "pod_total": pod_total,
                "pod_request": pod_total,
                "service_total": service_total,
                "node_total": node_total,
                "api_server": commpent["api_server"],
                "proxy": commpent["proxy"],
                "kubelet": commpent["proxy"],
                "cmanager": commpent["controller-manager"],
                "etcd": commpent["etcd"],
                "scheduler": commpent["scheduler"],
            }
        }  #

    def get_node_infos(self):
        pass


class ClusterManger_Controller():
    def install_new_cluster(self):
        pass


class RBAC_Controller():
    config_path, common_prom = load_config()
    context = "kubernetes-admin@cluster.local"
    config.load_kube_config(config_path, context=context)
    rbac = client.RbacAuthorizationV1Api()

    def __int__(self):
        self.rbac = client.RbacAuthorizationV1Api()

    def add_role(self, role_namespace, role_name, role_rule_apiGroups, role_rule_resources, role_rule_verbs):
        # rbac = client.RbacAuthorizationV1Api()
        body = k8s_yaml_helper.kuberntes_role(role_namespace, role_name, role_rule_apiGroups, role_rule_resources,
                                              role_rule_verbs)
        self.rbac.create_namespaced_role(namespace=role_namespace, body=body)

    def delete_role(self, role_name, namespace):
        self.rbac.delete_namespaced_role(name=role_name, namespace=namespace)

    def list_all_roles(self):
        return self.rbac.list_cluster_role_binding()

    def add_role_bind_user(self, config, user, namespace, day, rolename):
        # add new key and crt and  kubectl config
        os_controller.add_k8sconfig_on_master(config, user, namespace, day)
        # bind role to user
        body = k8s_yaml_helper.kuberentes_role_binding(user, namespace, rolename)
        self.rbac.create_namespaced_role_binding(namespace=namespace, body=body)
        relation = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        db_controller.insert_user_role(user_name=user, namespace=namespace, relation_id=relation, role_status="1")
        # example:
        # user_config={"name":"","ip":'',"port":,"user":"","pwd":""}
        # add_role_bind_user(user_config,"test4","test","365","myrole2")


# user_config={"name":"myrole","ip":'192.168.56.104',"port":22,"user":"root","pwd":"xta"}
# RBAC_Controller().add_role_bind_user(user_config,"test6","test","365","myrole2")
# print(RBAC_Controller().list_all_roles())


class Service_Controller():
    config_path, common_prom = load_config()
    context = "kubernetes-admin@cluster.local"
    config.load_kube_config(config_path, context=context)

    def __int__(self):
        self.svc = client.CoreV1Api

    def create_service(self, namespace, body):
        self.svc.create_namespaced_service(namespace=namespace, body=body)


#
# v1=None
# extenapi=None


class V1_Controller():
    def get_namespace(self):
        v1, extenapi = load_current_config()
        json = {"namespaces": [], "total": 0}
        num = 0
        for ns in v1.list_namespace().items:
            json["namespaces"].append(
                {"name": ns.metadata.name,
                 "status": ns.status.phase,
                 "create_time": ns.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")})
            num = num + 1
        json["total"] = num
        return json

    def get_namespace_by_name(self, name):
        v1, extenapi = load_current_config()
        json = {"namespaces": [], "total": 0}
        num = 0
        # json_item=[x for x in v1.list_namespace().items if x.metadata.name == name]
        for ns in v1.list_namespace().items:
            if ns.metadata.name == name:
                json["namespaces"].append(
                    {"name": ns.metadata.name,
                     "status": ns.status.phase,
                     "create_time": ns.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")})
                num = num + 1
        json["total"] = num
        return json

    def check_namespace_exists(self, name):
        v1, extenapi = load_current_config()
        is_exist = False
        json_item = [x for x in v1.list_namespace().items if x.metadata.name == name]
        if len(json_item) > 0:
            is_exist = True
        else:
            is_exist = False
        return is_exist

    def create_namespace(self, name):
        v1, extenapi = load_current_config()
        body = {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": name, }
        }
        v1.create_namespace(body=body, async_req=True)

    def get_all_pod_infos(self):
        v1, extenapi = load_current_config()
        pod_list = {"pods": [], "total": 0}
        num = 0
        reg_list = v1.list_pod_for_all_namespaces().items
        for pod in reg_list:
            my_date = pod.status.start_time
            pod_list["pods"].append(
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "node_name": pod.spec.node_name,
                    "node_ip": pod.status.host_ip,
                    "pod_ip": pod.status.pod_ip,
                    "start_time": my_date

                }
            )
            num = num + 1
        pod_list["total"] = num
        return pod_list

    def get_node_infos(self):
        v1, extenapi = load_current_config()
        node_list = {"node": [], "total": 0}
        num = 0
        reg_list = v1.list_node().items
        for node in reg_list:
            node_address = ""
            for address in node.status.addresses:
                if address.type == "InternalIP":
                    node_address = address.address
            node_list["node"].append(
                {
                    "name": node.metadata.name,
                    "address": node_address,
                    "os": node.status.node_info.os_image,
                    "docker_version": node.status.node_info.container_runtime_version,
                    "kubelet_version": node.status.node_info.kubelet_version
                }
            )
            num = num + 1
        node_list["total"] = num
        return node_list

    def get_images_infos(self):
        v1, extenapi = load_current_config()
        images_list = {"images": [], "total": 0, "node_list": []}
        reg_list = v1.list_node().items
        num = 0
        for node in reg_list:
            node_name = node.metadata.name
            if node_name not in images_list["node_list"]:
                images_list["node_list"].append(node_name)
            for img in node.status.images:
                for name in img.names:
                    if "sha256" not in str(name):
                        size = img.size_bytes
                        print(name)
                        if str(name) == None or str(name) == "" or name == "<none>@<none>":
                            images_list["images"].append(
                                {
                                    "node_name": node_name,
                                    "name": str(name).split('@')[0],  # "version":version,
                                    "version": str(name).split('@')[1],
                                    "size": size

                                })
                            num = num + 1
                        else:
                            images_list["images"].append(
                                {
                                    "node_name": node_name,
                                    "name": str(name).split(':')[0],  # "version":version,
                                    "version": str(name).split(':')[1],
                                    "size": size

                                })
                            num = num + 1
        images_list['total'] = num
        return images_list

    def get_imgaes_by_arg(self, node_name, name):
        list = self.get_images_infos()
        search_list = {"images": [], "total": 0, "node_list": []}
        search_list["node_list"] = list["node_list"]
        num = 0
        for img in list["images"]:
            if name == None or name == "":
                if img["node_name"] == node_name:
                    search_list["images"].append(img)
                    num = num + 1
            else:
                if img["node_name"] == node_name and img["name"] == name:
                    search_list["images"].append(img)
                    num = num + 1
        search_list["total"] = num
        return search_list

    def get_apps(self):
        v1, extenapi = load_current_config()

        result = {"apps": [], "total": 0}
        num = 0
        list = []
        for deploy in extenapi.list_deployment_for_all_namespaces().items:
            state = "Error"
            if deploy.status.replicas == deploy.status.ready_replicas:
                state = "Running"
            list.append(
                {
                    "name": deploy.metadata.name,
                    "namespace": deploy.metadata.namespace,
                    "images": deploy.spec.template.spec.containers[0].image,
                    "replicas": deploy.status.replicas,
                    "ready_replicas": deploy.status.ready_replicas,
                    "status": state,
                    "sourcetype": "Deployment"
                }
            )
            num = num + 1
        for daemonset in CoreAppApiV1().list_daemonsets_for_all_namespaces().items:
            state = "Error"
            if daemonset.status.current_number_scheduled == daemonset.status.number_ready:
                state = "Running"
            list.append(
                {
                    "name": daemonset.metadata.name,
                    "namespace": daemonset.metadata.namespace,
                    "images": daemonset.spec.template.spec.containers[0].image,
                    "replicas": daemonset.status.current_number_scheduled,
                    "ready_replicas": daemonset.status.number_ready,
                    "status": state,
                    "sourcetype": "DaemonSet"
                }
            )
            num = num + 1
        for statefulset in CoreAppApiV1().list_statefulset_for_all_namespaces().items:
            state = "Error"
            if statefulset.status.replicas == statefulset.status.ready_replicas:
                state = "Running"
            list.append(
                {
                    "name": statefulset.metadata.name,
                    "namespace": statefulset.metadata.namespace,
                    "images": statefulset.spec.template.spec.containers[0].image,
                    "replicas": statefulset.status.replicas,
                    "ready_replicas": statefulset.status.ready_replicas,
                    "status": state,
                    "sourcetype": "statefulset"
                }
            )
            num = num + 1
        result["apps"] = list
        result["total"] = num
        return result

    def get_all_service(self):
        v1, extenapi = load_current_config()
        result = {"service": [], "total": 0}
        v1.list_service_for_all_namespaces()

    def get_pod_by_namespace(self, namespace):
        v1, extenapi = load_current_config()
        pod_list = {"pods": [], "total": 0}
        num = 0
        reg_list = v1.list_namespaced_pod(namespace).items
        for pod in reg_list:
            my_date = pod.status.start_time
            pod_list["pods"].append(
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "node_name": pod.spec.node_name,
                    "node_ip": pod.status.host_ip,
                    "pod_ip": pod.status.pod_ip,
                    "start_time": my_date

                }
            )
            num = num + 1
        pod_list["total"] = num
        return pod_list


class AppControllor():
    config_path, common_prom = load_config()
    context = "kubernetes-admin@cluster.local"
    config.load_kube_config(config_path, context=context)
    app_api = client.AppsV1Api()

    def __int__(self, namespace, body):
        self.namespace = namespace
        self.body = body

    def create_deploy_app(self):
        self.app_api.create_namespaced_deployment(namespace=self.namespace, body=self.body)

    def delete_deploy_app(self, name):
        self.app_api.delete_namespaced_deployment(namespace=self.namespace, name=name)

    def apply_deploy_app(self, name):
        self.app_api.replace_namespaced_deployment(namespace=self.namespace, name=name, body=self.body)

# deploy = {
#     "name": "nginx",
#     "replicas": 2,
#     "image": "nginx:1.15",
#     "cpu": "0.1",
#     "memory": "200Mi"
# }
#
# appcontroller = AppControllor()
# appcontroller.body = k8s_yaml_helper.kubernetes_deployment(deploy)
# appcontroller.namespace = "default"
