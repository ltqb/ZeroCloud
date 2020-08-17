import subprocess

import ansible_runner

from controller import db_controller


class InventoryHelper():
    def get_keys_line(self, jlist):
        list = []
        for myinfo in jlist:
            for info in myinfo:
                ansible_name = info
                line = ""
                for str_key in myinfo[info]:
                    current_line = "    " + str_key + "=" + myinfo[info][str_key]
                    line = line + current_line
                list.append(ansible_name + "  " + line)
        return list

    def get_lines(self, title, mylist):
        list = self.get_keys_line(mylist)
        first_line = "[" + title + "]\n"
        line = ""
        for mystr in list:
            line = line + mystr + "\n"
        result = first_line + line
        return result

    def write_inventory(self, dst_file, title, jsonlist):
        with open(dst_file, 'w') as f:
            lines = self.get_lines(title, jsonlist)
            f.write(lines)
            f.close()


data_dir = "/opt/ansible"
inventory_file = "/opt/app_config/inventory.ini"
inventory_list = []


def write_inventory_from_db():
    all_host_info = db_controller.get_all_hosts_info()
    for str in all_host_info:
        inventory_list.append(
            {str.name: {
                "ansible_host": str.ip_address,
                "ansible_user": str.user_name,
                "ansible_ip": str.ip_address,
                "ansible_password": str.user_password}
            }
        )
    inventory_helper = InventoryHelper()
    inventory_helper.write_inventory(inventory_file, "all", inventory_list)


def get_all_host_fact():
    write_inventory_from_db()
    rc = ansible_runner.RunnerConfig(private_data_dir=data_dir, module="setup", module_args='',
                                     host_pattern='all', quiet=True,
                                     forks=len(inventory_list),
                                     inventory=inventory_file,
                                     json_mode=True
                                     )

    rc.prepare()

    r = ansible_runner.Runner(config=rc)
    r.run()
    fact_list = []
    for mystrs in inventory_list:
        for str in mystrs:
            myfact = r.get_fact_cache(str)
            fact_list.append({
                "ansible_name": str,
                "facts": myfact}
            )
    # print(fact_list)
    return fact_list


def ping_host(host):
    result = subprocess.getoutput("ping -c 1 " + host)
    if "ttl" in result or "TTL" in result:
        return {"host": host, "result": True}
    else:
        return {"host": host, "result": False}


def write_host_state_2_db(json_fact):
    result = []
    for myfact in json_fact:
        name = myfact["ansible_name"]
        if "ansible_processor_cores" in myfact["facts"].keys():
            cpu_count = myfact["facts"]["ansible_processor_cores"]
            mem_count = myfact["facts"]["ansible_memtotal_mb"]
            db_controller.edit_host_info(name, "remark",
                                         str(cpu_count) + "核 " + str(int(round(mem_count / 1024, 0))) + "G")
            db_controller.edit_host_info(name, "device_status", "running")
            result.append({"ansible_name": name, "status": True})
        else:
            db_controller.edit_host_info(name, "device_status", "offline")
            result.append({"ansible_name": name, "status": False})
    return result
