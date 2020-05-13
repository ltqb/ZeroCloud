import sys

import paramiko

list={"name":None,"percent":[0,]}



sjl01={
    "name":"sjl01",
    "ip":'172.16.200.4',
    "port":22,
    "user":"root",
    "pwd":"Happytime2020!"
}
sjl02={
    "name":"sjl02",
    "ip":'172.16.200.5',
    "port":22,
    "user":"root",
    "pwd":"Happytime2020!"
}
sjl03={
    "name":"sjl03",
    "ip":'172.16.200.6',
    "port":22,
    "user":"root",
    "pwd":"Happytime2020!"
}

nodeinfos=[]
nodeinfos.append(sjl01)
nodeinfos.append(sjl02)
nodeinfos.append(sjl03)


def progress_bar(transferred, toBeTransferred):
    bar_len = 100
    filled_len = int(round(bar_len * transferred / float(toBeTransferred)))
    list["percent"].append(filled_len)


class SSHConnection(object):

    def __init__(self, config):
        self.host = config["ip"]
        self.port = config["port"]
        self.username = config["user"]
        self.pwd = config["pwd"]
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def get(self, target_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(target_path, local_path,callback=progress_bar)


    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        err=stderr.read()
        return result,err


def ssh_cmd(config,cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=config["ip"], port=config["port"], username=config["user"], password=config["pwd"])
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    errstr=stderr.read()
    ssh.close
    return result,errstr



def  docker_images_download(node_name,image_name,save_name,local_path):
    for info in nodeinfos:
        if node_name ==info["name"]:
            list["name"] = local_path
            list["percent"]=[0,]
            conn=SSHConnection(info)
            conn.connect()
            result,err=conn.cmd("docker save "+image_name+" -o "+save_name)
            if err==b'':
                conn.get(save_name,local_path)
                print("success",err)
            else:
                print("save fail")
            conn.close()



#docker_images_download("sjl01","jimmidyson/configmap-reload:v0.2.2","/tmp/configmap-reload-v0.2.2.tar","configmap-reload-v0.2.2.tar")

