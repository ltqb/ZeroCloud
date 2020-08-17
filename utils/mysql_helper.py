import datetime

import pymysql
from sqlalchemy import create_engine
from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import functions
from werkzeug.security import generate_password_hash

pymysql.install_as_MySQLdb()
engine = create_engine("mysql+pymysql://@212.64.85.14:33306/container_cloud", encoding='utf-8', echo=True)
base = declarative_base()
DBSession = sessionmaker(bind=engine)


class UserInfo(base):
    __tablename__ = 'user_info'  # 表名
    id = Column(Integer, primary_key=True)
    user_id = Column(String(32))
    user_name = Column(String(32))
    user_password = Column(String(64))
    user_phone = Column(String(11))
    user_email = Column(String(32))
    user_role = Column(String(32))
    remark = Column(String(128))
    row_status = Column(Integer, default=1)
    create_time = Column(DateTime, default=datetime.datetime.now())
    update_time = Column(DateTime, default=datetime.datetime.now())

    def __int__(self, user_id, user_name, user_password, user_phone, user_email, remark, create_time, update_time,
                user_role, row_status):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password
        self.user_phone = user_phone
        self.user_email = user_email
        self.remark = remark
        self.create_time = create_time
        self.update_time = update_time
        self.user_role = user_role
        self.row_status = row_status


class RoleInfo(base):
    __tablename__ = 'role_info'  # 表名
    id = Column(Integer, primary_key=True)
    role_id = Column(String(32))
    role_name = Column(String(64))
    role_namespace = Column(String(64))
    role_rule_apiGroups = Column(String(255))
    role_rule_resources = Column(String(255))
    role_rule_verbs = Column(String(255))
    row_status = Column(Integer, default=1)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    def __int__(self, role_id, role_name, role_namespace, role_rule_apiGroups,
                role_rule_resources, role_rule_verbs, create_time, update_time, row_status):
        self.role_id = role_id
        self.role_name = role_name
        self.role_namespace = role_namespace
        self.role_rule_apiGroups = role_rule_apiGroups
        self.role_rule_resources = role_rule_resources
        self.role_rule_verbs = role_rule_verbs
        self.create_time = create_time
        self.update_time = update_time
        self.row_status = row_status


class UserRole(base):
    __tablename__ = 'user_role'  # 表名
    id = Column(Integer, primary_key=True)
    relation_id = Column(String(32))
    user_id = Column(String(64))
    role_id = Column(String(64))
    namespace = Column(String(128))
    role_status = Column(String(64))
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    def __int__(self, relation_id, user_id, role_id,namespace, role_status, create_time, update_time):
        self.relation_id = relation_id
        self.user_id = user_id
        self.role_id = role_id
        self.namespace = namespace
        self.role_status = role_status
        self.create_time = create_time
        self.update_time = update_time


class MenuInfo(base):
    __tablename__ = 'menu_info'  # 表名
    id = Column(Integer, primary_key=True)
    menu_id = Column(String(32))
    menu_name = Column(String(64))
    menu_json = Column(String(255))
    menu_status = Column(Integer, default=1)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    def __int__(self, menu_id, menu_name, menu_json, menu_status, create_time, update_time):
        self.menu_id = menu_id
        self.menu_name = menu_name
        self.menu_json = menu_json
        self.menu_status = menu_status
        self.create_time = create_time
        self.update_time = update_time


class Config_file(base):
    __tablename__ = 'config_file'  # 表名
    id = Column(Integer, primary_key=True)
    config_name = Column(String(64))
    config_path = Column(String(255))
    config_status = Column(Integer, default=1)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    def __int__(self, config_name, config_path, config_status, create_time, update_time):
        self.config_name = config_name
        self.config_path = config_path
        self.config_status = config_status
        self.create_time = create_time
        self.update_time = update_time


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
    own_cluster = Column(String(32))

    # row_status = Column(Integer, default=1)

    def __int__(self, name, ip_address, mac_address, user_name, user_password, ssh_port, device_type, location, remark,
                create_time, update_time, device_status, own_cluster, row_status):
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
        self.own_cluster = own_cluster
        # self.row_status = row_status


class BaseView():
    def __int__(self, table_view):
        self.view = table_view

    def find_all(self):
        session = DBSession()
        all = session.query(self.view).all()
        session.close()
        return all

    def insert_row(self, view):
        session = DBSession()
        session.add(view)
        session.commit()
        session.close()

    def find_one(self, key, data):
        session = DBSession()
        my_view = session.query(self.view).filter(getattr(self.view, key) == data).first()
        session.close()
        return my_view

    def modify_one(self, id, key, data):
        session = DBSession()
        my_view = session.query(self.view).filter(self.view.id == id).first()
        setattr(my_view, key, data)
        session.commit()
        session.close()
        return my_view

    def modify_one_by_name(self, name, key, data):
        session = DBSession()
        my_view = session.query(self.view).filter(self.view.name == name).first()
        setattr(my_view, key, data)
        session.commit()
        session.close()
        return my_view

    def modify_inst(self, inst, key, data):
        session = DBSession()
        my_view = session.query(self.view).filter(self.view == inst)
        setattr(my_view, key, data)
        session.commit()
        session.close()
        return my_view

    def soft_delete(self, id):
        session = DBSession()
        my_view = session.query(self.view).filter(self.view.id == id).first()
        my_view.row_status = 0
        session.commit()
        session.close()
        return my_view

    def hard_delete(self, view):
        session = DBSession()
        # my_view = session.query(self.view).filter(self.view.id == id).first()
        session.delete(view)
        session.commit()
        session.close()

    def max_id(self):
        session = DBSession()
        max_id = session.query(functions.max(self.view.id)).scalar()
        session.close()
        return max_id

    # aaaa=BaseView()
    # aaaa.view=UserInfo
    # bbbbb=aaaa.max_id()
    # print(bbbbb)

    def check_name_is_exists(self, key, name):
        session = DBSession()
        my_name = session.query(self.view).filter(getattr(self.view, key) == name).count()
        if my_name == 0:
            session.close()
            return False
        else:
            session.close()
            return True

# class DeviceView():
#     def find_all(self):
#         return session.query(DeviceInfo).all()
#
#     def insert_device(self, name, ip_address, mac_address, user_name, user_password, ssh_port, device_type, location,
#                       remark, create_time, update_time, device_status):
#         session.add(DeviceInfo(name=name,
#                                ip_address=ip_address,
#                                mac_address=mac_address,
#                                user_name=user_name,
#                                user_password=user_password,
#                                ssh_port=ssh_port,
#                                device_type=device_type,
#                                location=location,
#                                remark=remark,
#                                create_time=create_time,
#                                update_time=update_time,
#                                device_status=device_status))
#         session.commit()
#         session.close()
#
#     def find_one(self, id):
#         my_device = session.query(DeviceInfo).filter(DeviceInfo.id == id).first()
#         return my_device
#
# myView=BaseView()
# myView.view=UserInfo
# add=UserInfo()
# add.user_name="admin"
# add.user_password="admin@123"
# add.user_role="99999"
# myView.insert_row(add)


# def get_all_device_to_list():
#     myinfo = DeviceView()
#     num = 0
#     list = []
#     for info in myinfo.find_all():
#         list.append(
#             {
#                 "hostname": info.name,
#                 "ip_address": info.ip_address,
#                 "mac_address": info.mac_address,
#                 "remark": info.remark,
#                 "create_time": info.create_time.strftime("%Y-%m-%d %H:%M:%S"),
#                 "device_status": info.device_status,
#                 "own_cluster": info.own_cluster
#             }
#         )
#         num = num + 1
#     result = {
#         "devices": list,
#         "device_total": num
#     }
#     return result


base.metadata.create_all(engine)
