## 开发环境
- python3.6
- flask 框架
- 前端vue-manager-system框架

## 依赖
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

## 部署

- docker部署

```powershell
docker build -t zero_cloud:v1.0.1 .

docker run -d -p5000:5000  --name=zero_cloud zero_cloud:v1.0.1
```
- 宿主机部署测试
```powershell
python3 app.py
```

## 主要功能

- 多租户设计，实现容器云的多租户使用 （管理员权限）

- 基于k8s集群的容器云，集群管理，集群节点自动横向扩展，集群状态概览 （管理员权限）

- 容器管理，镜像管理，POD管理 ,容器日志的管理,（运维角色）

- 应用持续发布交付，应用更新，服务的管理 （运维开发角色）

- 容器云的监控告警，基于promethues（管理员权限）

## 联系方式
- QQ : 42188007
- Email: 42188007@qq.com

## 界面展示：

示例演示地址：
http://212.64.85.14/


![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/b0999dc299f2dd08d66cde90b59a6ed.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/53c3747e65ab9ca82c1909d588432ea.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/0123ba3a97e25faf9c40f6c31c9b6de.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/99cfdf45f05e1ad84c30596fa3ae502.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/9f1a531d348ea6882bcbb01721b9f8d.png)

![image](https://github.com/EthanSun2019/ZeroCloud/blob/master/img/a2b51d12c1af2df1b76a3d600079a90.png)


