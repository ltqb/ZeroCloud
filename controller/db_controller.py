import datetime
import json

from werkzeug.security import generate_password_hash, check_password_hash

from utils import mysql_helper


def generate_menu(user_name):
    user_controller = mysql_helper.BaseView()
    user_controller.view = mysql_helper.UserInfo
    list_menu = []
    if user_controller.check_name_is_exists("user_name", user_name) == True:
        user_info = user_controller.find_one("user_name", user_name)
        if user_info.user_name == user_name and user_info.user_role == "99999":
            menu_controller = mysql_helper.BaseView()
            menu_controller.view = mysql_helper.MenuInfo
            menu_info = menu_controller.find_all()
            for menu in menu_info:
                list_menu.append(menu.menu_json)
        if user_info.user_name == user_name and user_info.user_role == "9":
            menu_controller = mysql_helper.BaseView()
            menu_controller.view = mysql_helper.MenuInfo
            menu_info = menu_controller.find_all()
            for menu in menu_info:
                if menu.id == 2:
                    list_menu.append(menu.menu_json)
    return list_menu


def generate_user_id(max_id, total_length):
    max_id = int(max_id) + 1
    max_id = str(max_id)
    user_id = str.rjust(max_id, total_length, "0")
    return user_id


def insert_user_info(user_name, user_pwd, user_email, phone):
    user_controller = mysql_helper.BaseView()
    user_controller.view = mysql_helper.UserInfo
    if user_controller.check_name_is_exists("user_name", user_name) == False:
        my_info = mysql_helper.UserInfo()
        my_info.user_id = generate_user_id(user_controller.max_id(), 5)
        my_info.user_name = user_name
        my_info.user_password = generate_password_hash(user_pwd)
        my_info.user_email = user_email
        my_info.user_phone = phone
        my_info.row_status = -1
        my_info.user_role = "0"
        user_controller.insert_row(my_info)
        return {"result": "ok"}
    else:
        return {"result": "exists"}


def insert_user_role(user_name, namespace, relation_id, role_status):
    user_role_controller = mysql_helper.BaseView()
    user_role_controller.view = mysql_helper.UserRole
    if user_role_controller.check_name_is_exists("relation_id", relation_id) == False:
        my_info = mysql_helper.UserRole()
        my_info.relation_id = relation_id
        my_info.user_id = user_name
        my_info.namespace = namespace
        my_info.role_status = role_status
        my_info.create_time = datetime.datetime.now()
        my_info.update_time = datetime.datetime.now()
        user_role_controller.insert_row(my_info)


# insert_user_role("xiaoli","test","20001","1")

def add_role_menu_to_user(user_name, user_role, row_status):
    user_controller = mysql_helper.BaseView()
    user_controller.view = mysql_helper.UserInfo
    if user_controller.check_name_is_exists("user_name", user_name) == True:
        user_id = user_controller.find_one("user_name", user_name).id
        user_controller.modify_one(user_id, "user_role", user_role)
        user_controller.modify_one(user_id, "row_status", row_status)


def auth_user_info(user_name, user_pwd):
    user_controller = mysql_helper.BaseView()
    user_controller.view = mysql_helper.UserInfo
    if user_controller.check_name_is_exists("user_name", user_name) == False:
        print("user name not exists ,please apply for an account")
        return {"auth_state": False, "menu_role": "0"}
    else:
        my_user = user_controller.find_one("user_name", user_name)
        if check_password_hash(my_user.user_password, user_pwd) == True and my_user.row_status == 1:

            return {"auth_state": True, "menu_role": my_user.user_role}
        else:
            return {"auth_state": False, "menu_role": "0"}


# add_role_menu_to_user("admin","99999",1)

# print(auth_user_info("admin", "admin@123"))


def get_all_hosts_info():
    device_controller = mysql_helper.BaseView()
    device_controller.view = mysql_helper.DeviceInfo
    info = device_controller.find_all()
    return info


def add_host_info(name, ip_address, user_name, user_password, ssh_port, device_type, location, remark,
                  own_cluster):
    try:
        device_controller = mysql_helper.BaseView()
        device_controller.view = mysql_helper.DeviceInfo
        if device_controller.check_name_is_exists("name", name) == False:
            my_info = mysql_helper.DeviceInfo()
            my_info.name = name
            my_info.user_name = user_name
            my_info.user_password = user_password
            my_info.ip_address = ip_address
            my_info.ssh_port = ssh_port
            my_info.device_type = device_type
            my_info.location = location
            my_info.remark = remark
            my_info.create_time = datetime.datetime.now()
            my_info.update_time = datetime.datetime.now()
            my_info.device_status = "unknown"
            my_info.own_cluster = own_cluster
            device_controller.insert_row(my_info)
            return {"result": 1}
        else:
            return {"result": 0}
    except:
        return {"result": 0}


def delete_host_info(name):
    try:
        device_controller = mysql_helper.BaseView()
        device_controller.view = mysql_helper.DeviceInfo
        myinfo = device_controller.find_one("name", name)
        device_controller.hard_delete(myinfo)
        return {"result": 1}
    except:
        return {"result": 0}


def edit_host_info(name, hostkey, hostvalue):
    device_controller = mysql_helper.BaseView()
    device_controller.view = mysql_helper.DeviceInfo
    # myinfo = device_controller.find_one("name", name)
    device_controller.modify_one_by_name(name, hostkey, hostvalue)


def get_config_file():
    config_controller = mysql_helper.BaseView()
    config_controller.view = mysql_helper.Config_file
    info = config_controller.find_all()
    return info
# print(delete_host_info("test5")

# my=DeviceView()
# my.add_host_info("test","127.0.0.1","root","password",22,0,"1F","2核 8G","")
# get_all_hosts_info()
