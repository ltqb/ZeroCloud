## Environment
- python3.6
- flask Framework
- vue-manager-system framework

## Installed packages
- kubernetes==11.0.0
- flask==1.1.2
- docker==4.2.0
- sqlalchemy==1.3.16
- werkzeug==1.0.1
- pymysql==0.9.3
- paramiko==2.7.1
- dateparser==0.7.6
- retrying==1.3.3
- ansible==2.7.8
- jinja2==2.9.6
- netaddr
- pbr==1.6
- hvac
- jmespath
- ruamel.yaml
- ansible_runner

## Deployment

- docker deployment

```powershell
docker build -t zero_cloud:v1.0.1 .

docker run -d -p5000:5000  --name=zero_cloud zero_cloud:v1.0.1
```
- Run
```powershell
python3 app.py
```

## Functions

- Design for multi user,and users can use self space or namespace of caontainer cloud (admin)

- The Container cloud base on kubernetes ,Cluster manager, node auto scaler and status of the container cloud（admin）

- Container Manager ,docker image manager,pod manager,container log manager (ops)

- CICD,Deployment and sevice manager (devops）

- Monitor and alertment of container cloud ,base on prometheus (ops)

## Contact
- QQ : 42188007
- Email: 42188007@qq.com

## Pictrure Show：

Demo address：
http://212.64.85.14/


![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/img/b0999dc299f2dd08d66cde90b59a6ed.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/img/53c3747e65ab9ca82c1909d588432ea.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/img/0123ba3a97e25faf9c40f6c31c9b6de.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/img/99cfdf45f05e1ad84c30596fa3ae502.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/img/9f1a531d348ea6882bcbb01721b9f8d.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/img/a2b51d12c1af2df1b76a3d600079a90.png)


