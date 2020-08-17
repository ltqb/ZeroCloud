import subprocess

# return1 = subprocess.getoutput("ping -n 1 192.168.56.21")
#
# if "ttl" in return1 or "TTL" in return1:
#     print("1")
# else:
#     print("0")
import toml

a=toml.load("config.toml")
print(a["clusters"])