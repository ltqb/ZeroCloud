import paramiko

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
        err = stderr.read()
        return result, err


def add_k8sconfig_on_master(config, user, namespace, day):
    myssh = SSHConnection(config)
    myssh.connect()
    path = "/usr/etc/ssl/" + user + "/"
    user_key = path + user + ".key"
    user_csr = path + user + ".csr"
    user_crt = path + user + ".crt"
    myssh.cmd("mkdir " + path)
    myssh.cmd("openssl genrsa -out " + user_key + " 2048")
    csr_str="openssl req -new -key " + user_key + " -out " + user_csr + " -subj '/CN=" + user + "/O="+namespace+"'"
    myssh.cmd(csr_str)
    myssh.cmd(
        "openssl x509 -req -in " + user_csr + " -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out " + user_crt + " -days " + day)
    myssh.cmd(
        "kubectl config set-credentials " + user + " --client-certificate=" + user_crt + " --client-key=" + user_key)
    myssh.cmd(
        "kubectl config set-context "+user+"-context --cluster=cluster.local --namespace="+namespace+" --user="+user)




