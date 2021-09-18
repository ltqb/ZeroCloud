import subprocess
import toml
# test file
a=toml.load("config.toml")
print(a["clusters"])
