import datetime

import docker

client = docker.APIClient(base_url='unix:/var/run/docker.sock', timeout=5)

def get_docker_version():
    data = client.version()
    print(data)
    return {"Version": data["Version"],
            "GoVersion": data["GoVersion"],
            "Os_Arch": data["Os"] + "/" + data["Arch"],
            "KernelVersion": data["KernelVersion"],
            "BuildTime": data["BuildTime"]}

def get_docker_images():
    data = client.images()
    list = []
    for my in data:
        list.append({'Created': my["Created"],
                     'Id': my["Id"],
                     'Labels': my["Labels"],
                     'ParentId': my["ParentId"],
                     'RepoDigests': my["RepoDigests"],
                     'RepoTags': my["RepoTags"],
                     'SharedSize': my["SharedSize"],
                     'Size': my["Size"],
                     'VirtualSize': my["VirtualSize"]})
    return list

def push_image(image):
    for line in client.push(image, stream=True, decode=True):
        print(line)

def tag_image(image, repo):
    bool = client.tag(image, repository=repo, force=True)
    return bool

def get_all_containers():
    data = client.containers(all=True)
    num = 0
    list = []

    for my in data:
        name = ""
        if "/" in my["Names"][0]:
            name = str(my["Names"][0]).split('/')[1]
        list.append(
            {
                'Id': my["Id"],
                'Names': name,
                'Image': my['Image'],
                'ImageID': my['ImageID'],
                'Command': my['Command'],
                'Created':
                    datetime.datetime.strftime(datetime.datetime.fromtimestamp(my['Created']), '%Y-%m-%d %H:%M:%S'),
                'Ports': my['Ports'],
                'Labels': my['Labels'],
                'State': my['State'],
                'Status': my['Status'],
                'HostConfig': my['HostConfig'],
                'NetworkSettings': my['NetworkSettings'],
                'Mounts': my['Mounts']
            }
        )
        num = num + 1
    result = {"containers": list, "total": num}
    return result

def remove_container(container):
    try:
        client.remove_container(container, force=True)
        return {"optype": "rm", "result": "success"}
    except:
        return {"optype": "rm", "result": "fail"}

def start_container(cont):
    try:
        client.start(cont)
        return {"optype": "start", "result": "success"}
    except:
        return {"optype": "start", "result": "fail"}

def stop_container(cont):
    try:
        client.stop(cont)
        return {"optype": "stop", "result": "success"}
    except:
        return {"optype": "stop", "result": "fail"}

def restart_container(cont):
    try:
        client.restart(cont)
        return {"optype": "restart", "result": "success"}
    except:
        return {"optype": "restart", "result": "fail"}

def create_container(cont):
    try:
        client.create_container(cont)
        return {"optype": "create", "result": "success"}
    except:
        return {"optype": "create", "result": "fail"}
