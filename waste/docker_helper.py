import argparse
import os,sys

def command_to_list(command):
    p=os.popen(command).readlines()
    return p


def parse_arguments(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument("--todo",type=str,choices=["save","tag","load","push"],default=None,help="todo type for images : save ,tag ,push ,load")
    parser.add_argument("--name","-n",type=str,default=None,help="grep name for images")
    parser.add_argument("--oldstr","-O",type=str,default=None,help="the name for images before tag")
    parser.add_argument("--newstr","-N",type=str,default=None,help="the name for images after tag ")
    return parser.parse_args(argv)


#批量打包镜像
def docker_image_packer(name):
    pkg_list=command_to_list("docker images|grep "+name+"|awk '{print $1\":\"$2}'")
    for pkg in pkg_list:
        pkg_name=str(pkg).split("\n")[0]
        result_name=pkg_name.split("/")[-1].replace(":","-")+".tar"
        command_to_list("docker save "+pkg_name+" > "+result_name)
        print(pkg_name,result_name,"success")

#批量修改镜像tag
def docker_images_tag(name,url):
    pkg_list = command_to_list("docker images|grep " + name + "|awk '{print $1\":\"$2}'")
    for pkg in pkg_list:
        pkg_name = str(pkg).split("\n")[0]
        tag_name=pkg_name.replace(name,url)
        command_to_list("docker tag "+pkg_name+" "+tag_name)
        print(pkg_name,tag_name,"success")

#批量上传镜像到镜像仓库
def docker_images_push(name):
    pkg_list = command_to_list("docker images|grep " + name + "|awk '{print $1\":\"$2}'")
    for pkg in pkg_list:
        pkg_name = str(pkg).split("\n")[0]
        try:
            command_to_list("docker push "+pkg_name)
            print(pkg_name," push success")
        except :
            print(pkg_name," push fail")

#批量load当前目录下的镜像
def docker_imgaes_load():
      pkg_list=command_to_list("ls")
      for pkg in pkg_list:
          command_to_list("docker load -i "+pkg)
          print(pkg,"success")


input_args=sys.argv[1:]
args=parse_arguments(input_args)
if args.todo=="save":
    docker_image_packer(args.name)
elif args.todo=="tag":
    docker_images_tag(args.name,args.oldstr,args.newstr)
elif args.todo=="push":
    docker_images_push(args.name)
elif args.todo=="load":
    docker_imgaes_load()

