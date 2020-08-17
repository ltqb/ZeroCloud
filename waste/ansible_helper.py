import sys

# import paramiko
import ansible_runner

data_dir = "/root/flask-kubernetes/utils"

rc = ansible_runner.RunnerConfig(private_data_dir=data_dir,
                                 module="setup",
                                 module_args='',

                                 host_pattern='all',
                                 forks=1,
                                 inventory="inventory.ini",
                                 json_mode=True)

print(rc.generate_ansible_command())
rc.prepare()
r = ansible_runner.Runner(config=rc)
a = r.run()
print("{}: {}".format(r.status, r.rc))
for each_host_event in r.events:
    print(each_host_event['stdout'])

# for str in a:
#     print(a["ansible_processor_cores"])
# cpu = a['contacted']["10.147.19.123"]['ansible_facts']['ansible_processor'][1]
# print(cpu)
# r# = ansible_runner.runner.Runner(config=rc)
# r.run()

# # list = {"name": None, "percent": [0, ]}
#
#
# #
# # sjl01={
# #     "name":"sjl01",
# #     "ip":'172.16.200.4',
# #     "port":22,
# #     "user":"root",
# #     "pwd":"Happytime2020!"
# # }
# # sjl02={
# #     "name":"sjl02",
# #     "ip":'172.16.200.5',
# #     "port":22,
# #     "user":"root",
# #     "pwd":"Happytime2020!"
# # }
# # sjl03={
# #     "name":"sjl03",
# #     "ip":'172.16.200.6',
# #     "port":22,
# #     "user":"root",
# #     "pwd":"Happytime2020!"
# # }
#
# # nodeinfos=[]
# # nodeinfos.append(sjl01)
# # nodeinfos.append(sjl02)
# # nodeinfos.append(sjl03)
#
#
# def progress_bar(transferred, toBeTransferred):
#     bar_len = 100
#     filled_len = int(round(bar_len * transferred / float(toBeTransferred)))
#     list["percent"].append(filled_len)
#
#
# class SSHConnection(object):
#
#     def __init__(self, config):
#         self.host = config["ip"]
#         self.port = config["port"]
#         self.username = config["user"]
#         self.pwd = config["pwd"]
#         self.__k = None
#
#     def connect(self):
#         transport = paramiko.Transport((self.host, self.port))
#         transport.connect(username=self.username, password=self.pwd)
#         self.__transport = transport
#
#     def close(self):
#         self.__transport.close()
#
#     def get(self, target_path, local_path):
#         sftp = paramiko.SFTPClient.from_transport(self.__transport)
#         sftp.get(target_path, local_path, callback=progress_bar)
#
#     def cmd(self, command):
#         ssh = paramiko.SSHClient()
#         ssh._transport = self.__transport
#         # 执行命令
#         stdin, stdout, stderr = ssh.exec_command(command)
#         # 获取命令结果
#         result = stdout.read()
#         err = stderr.read()
#         return result, err
#
#
# def ssh_cmd(config, cmd):
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname=config["ip"], port=config["port"], username=config["user"], password=config["pwd"])
#     stdin, stdout, stderr = ssh.exec_command(cmd)
#     result = stdout.read()
#     errstr = stderr.read()
#     ssh.close
#     return result, errstr
#
# # def  docker_images_download(node_name,image_name,save_name,local_path):
# #     for info in nodeinfos:
# #         if node_name ==info["name"]:
# #             list["name"] = local_path
# #             list["percent"]=[0,]
# #             conn=SSHConnection(info)
# #             conn.connect()
# #             result,err=conn.cmd("docker save "+image_name+" -o "+save_name)
# #             if err==b'':
# #                 conn.get(save_name,local_path)
# #                 print("success",err)
# #             else:
# #                 print("save fail")
# #             conn.close()
#
#
# # docker_images_download("sjl01","jimmidyson/configmap-reload:v0.2.2","/tmp/configmap-reload-v0.2.2.tar","configmap-reload-v0.2.2.tar")

# r = ansible_runner.run(private_data_dir='/tmp/demo', module='shell', module_args='whoami')
# (module_name='setup', module_args='', pattern='all', forks=1, private_data_dir="inventory.ini")

# def get_info(ip):
#     data = {}
#     rur = runner.Runner(module_name='setup', module_args='', pattern='all', forks=1,private_data_dir="inventory.ini")
#     datastructure = rur.run()
#     print(datastructure)
#     sn = datastructure['contacted'][ip]['ansible_facts']['ansible_product_serial']
#     host_name = datastructure['contacted'][ip]['ansible_facts']['ansible_hostname']
#
#     description = datastructure['contacted'][ip]['ansible_facts']['ansible_lsb']['description']
#     ansible_machine = datastructure['contacted'][ip]['ansible_facts']['ansible_machine']
#     sysinfo = '%s %s' % (description, ansible_machine)
#
#     os_kernel = datastructure['contacted'][ip]['ansible_facts']['ansible_kernel']
#
#     cpu = datastructure['contacted'][ip]['ansible_facts']['ansible_processor'][1]
#     cpu_count = datastructure['contacted'][ip]['ansible_facts']['ansible_processor_count']
#     cpu_cores = datastructure['contacted'][ip]['ansible_facts']['ansible_processor_cores']
#     mem = datastructure['contacted'][ip]['ansible_facts']['ansible_memtotal_mb']
#
#     ipadd_in = datastructure['contacted'][ip]['ansible_facts']['ansible_all_ipv4_addresses'][0]
#     disk = datastructure['contacted'][ip]['ansible_facts']['ansible_devices']['sda']['size']
#     # print sysinfo
#     data['sn'] = sn
#     data['sysinfo'] = sysinfo
#     data['cpu'] = cpu
#     data['cpu_count'] = cpu_count
#     data['cpu_cores'] = cpu_cores
#     data['mem'] = mem
#     data['disk'] = disk
#     data['ipadd_in'] = ipadd_in
#     data['os_kernel'] = os_kernel
#     data['host_name'] = host_name
#
#     # return data
# get_info()
# data=get_info("10.147.19.123")
# print(data)
