def get_keys_line(jlist):
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


def get_lines(title, mylist):
    list = get_keys_line(mylist)
    first_line = "[" + title + "]\n"
    line = ""
    for mystr in list:
        line = line + mystr + "\n"
    result = first_line + line
    return result


def write_inventory(dst_file, title, jsonlist):
    with open(dst_file, 'w') as f:
        lines = get_lines(title, jsonlist)
        f.write(lines)
        f.close()
