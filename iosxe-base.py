from scrapli.driver.core import IOSXEDriver
from rich import print, print_json
import timeit

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

start = timeit.default_timer()
for device in devices:
    with IOSXEDriver(**device) as conn:
        interfaces = conn.send_command("show interfaces").genie_parse_output()
        hostname = conn.get_prompt()[:-1]
        # print_json(data=interfaces)
        
        for interface in interfaces.items():
            interface_name = interface[0]
            interface_info = interface[1]

            # print(f"checking {hostname} - {interface_name}")
            # print (f'  Interface is {interface_info["oper_status"]}, Last input: {interface_info["last_input"]}')
            # for ip in interface_info["ipv4"].items():
                # print(f'  IP {ip[1]["ip"]}, Prefix {ip[1]["prefix_length"]}')


            if interface_info["last_input"] == 'never':
                # print(f'  shutting down {interface_name}, set description "Shutdown by admin"')
                conn.send_configs(configs=[f'interface {interface_name}', 'description shutdown by admin', 'shut',], privilege_level="configuration")
                # result = conn.send_command("show interfaces")
                # (result.result)
        print('\n')
stop = timeit.default_timer()
print(stop-start)

import os

cwd = os.path.dirname(os.path.abspath(__file__))
print(cwd)

for device in devices:
    with IOSXEDriver(**device) as conn:
        running_cfg = conn.send_command("show running-config")
        hostname = conn.get_prompt()[:-1]
        save_location = os.path.join(cwd, f'{hostname}.bak')
        with open(save_location, 'w') as f:
            f.write(running_cfg.result)