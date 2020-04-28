import paramiko

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
        sftp.get(target_path, local_path)

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



def docker_images_download(node_name,image_name,save_name,local_path):
    for info in nodeinfos:
        if node_name ==info["name"]:
            conn=SSHConnection(info)
            conn.connect()
            result,err=conn.cmd("docker save "+image_name+" -o "+save_name)
            if err==b'':
                conn.get(save_name,local_path)
                print("success",err)
            else:
                print("save fail")
            conn.close()

#xsftp_get_helper("172.16.200.5",22,"root","Happytime2020!","/tmp/pause.tar","C:\\pause.tar")


docker_images_download("sjl01","kubespray-centos:2.10","/tmp/kubespray-centos-2.10.tar","images\\kubespray-centos-2.10.tar")

