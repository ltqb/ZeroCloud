def kuberntes_role(role_namespace, role_name, role_rule_apiGroups, role_rule_resources, role_rule_verbs):
    return {
        "kind": "Role",
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "metadata": {
            "namespace": role_namespace,
            "name": role_name
        },
        "rules": [{
            "apiGroups": role_rule_apiGroups,
            "resources": role_rule_resources,
            "verbs": role_rule_verbs
        }, ]
    }


def kuberentes_role_binding(user, namespace, role):
    return {
        "kind": "RoleBinding",
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "metadata": {
            "name": user,
            "namespace": namespace},
        "subjects": [{"kind": "User",
                      "name": user,
                      "apiGroup": "rbac.authorization.k8s.io", }],
        "roleRef": {
            "kind": "Role",
            "name": role,
            "apiGroup": "rbac.authorization.k8s.io"}
    }


def kubernetes_nodeport_service(namespace, app_label, service_name, container_port, svc_port,node_port):
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": service_name,
            "namespace": namespace
        },
        "spec": {
            "selector": {
                "app": app_label
            },
            "ports": {
                "port": svc_port,
                "targetPort": container_port,
                "nodePort": node_port
            },
            "type": "NodePort"}
    }
    # cluster_ip = {
    #     "apiVersion": "v1",
    #     "kind": "Service",
    #     "metadata": {
    #         "name": service_name,
    #         "namespace": namespace
    #     },
    #     "spec": {
    #         "selector": {
    #             "app": app_label},
    #         "ports": {
    #             "port": svc_port,
    #             "targetPort": container_port},
    #         "type": "ClusterIP"}


def kubernetes_deployment(deploy):
    body = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": deploy["name"],
            "labels": {
                "app": deploy["name"],
            }
        },
        "spec": {
            "replicas": deploy["replicas"],
            "template": {
                "metadata": {
                    "name": deploy["name"],
                    "labels": {
                        "app": deploy["name"]
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": deploy["name"],
                            "image": deploy["image"],
                            "resources": {
                                "limits": {
                                    "cpu": deploy["cpu"],
                                    "memory": deploy["memory"],

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
                    "app": deploy["name"]
                },
            }
        }
    }
    return body