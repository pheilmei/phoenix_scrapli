from scrapli.driver.core import IOSXEDriver
from rich import print
import os

cwd = os.path.dirname(os.path.abspath(__file__))
print(cwd)

router1 = {
 "host": "198.18.130.2",
 "auth_username": "admin",
 "auth_password": "C1sco12345",
 "auth_strict_key": False
}

router2 = {
 "host": "198.18.1.130",
 "auth_username": "admin",
 "auth_password": "C1sco12345",
 "auth_strict_key": False
}


devices = [router1, router2]

for device in devices:
    with IOSXEDriver(**device) as conn:
        hostname = conn.get_prompt()[:-1]
        interfaces = conn.send_command("show interfaces").genie_parse_output()

        print(interfaces)



