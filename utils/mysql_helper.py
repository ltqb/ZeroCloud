import datetime

from sqlalchemy import create_engine
from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:xta@212.64.85.14:13306/container_cloud", encoding='utf-8', echo=True)
base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()


class DeviceInfo(base):
    __tablename__ = 'device_info'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    ip_address = Column(String(32))
    mac_address = Column(String(32))
    user_name = Column(String(32))
    user_password = Column(String(64))
    ssh_port = Column(Integer, default=22)
    device_type = Column(Integer, default=1)
    location = Column(String(32))
    remark = Column(String(128))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    device_status = Column(String(32))

    def __int__(self, name, ip_address, mac_address, user_name, user_password, ssh_port, device_type, location, remark,
                create_time, update_time,device_status):
        self.name = name
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.user_name = user_name
        self.user_password = user_password
        self.ssh_port = ssh_port
        self.device_type = device_type
        self.location = location
        self.remark = remark
        self.create_time = create_time
        self.update_time = update_time
        self.device_status = device_status


class DeviceView():
    def find_all(self):
        return session.query(DeviceInfo).all()

    def insert_device(self, name, ip_address, mac_address, user_name, user_password, ssh_port, device_type, location,
                      remark, create_time, update_time,device_status):
        session.add(DeviceInfo(name=name,
                               ip_address=ip_address,
                               mac_address=mac_address,
                               user_name=user_name,
                               user_password=user_password,
                               ssh_port=ssh_port,
                               device_type=device_type,
                               location=location,
                               remark=remark,
                               create_time=create_time,
                               update_time=update_time,
                               device_status=device_status))
        session.commit()
        session.close()

    def find_one(self, id):
        my_device = session.query(DeviceInfo).filter(DeviceInfo.id == id).first()
        return my_device


def get_all_device_to_list():
    myinfo = DeviceView()
    num=0
    list = []
    for info in myinfo.find_all():
        list.append(
            {
                "hostname": info.name,
                "ip_address": info.ip_address,
                "mac_address": info.mac_address,
                "remark": info.remark,
                "create_time": info.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "device_status" :info.device_status
            }
        )
        num=num+1
    result={
        "devices":list,
        "device_total":num
    }
    return result


