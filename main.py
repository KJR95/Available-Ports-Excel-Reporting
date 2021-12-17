from netmiko import ConnectHandler
from netmiko import NetMikoAuthenticationException
from netmiko import NetMikoTimeoutException
import re
import csv
import getpass
import pandas as pd
from datetime import datetime

username = 'username'
password = 'password'  # getpass()
platform = 'arista_eos'
csv_file = 'PortData_' + str(datetime.now().strftime('%Y_%m_%d')) + '.csv'

with open(r'hostlist.txt', 'r') as IPS:
    with open(csv_file, 'w') as f:
        headerwriter = csv.DictWriter(f, fieldnames=['HOST', 'Datacenter', 'Free Ports'])
        headerwriter.writeheader()
        for line in IPS:
            writer = csv.writer(f)
            try:
                IPS = line.strip()
                device = ConnectHandler(device_type=platform, ip=IPS, username=username, password=password)
                output = device.send_command("show interface status")
                notconnectregex = len(re.findall(r"999", output))
                find_hostname = device.find_prompt()
                sshhost = find_hostname.replace("#","")
                datacentre = re.findall('DC1|DC2|DC3|DC4|ETC' , sshhost) #If name of datacentre is in hostname put it here to locate it to create a filter by DC on excel
                data = sshhost, '\n'.join(datacentre), notconnectregex
                writer.writerow(data)
                print(sshhost, '\n'.join(datacentre), 'Free Ports:', notconnectregex)
            except NetMikoAuthenticationException:
                print('Authentication error: Failed to connect to {}'.format(IPS))
            except NetMikoTimeoutException:
                print('Timeout error: Failed to connect to {}, Connection timed out'.format(IPS))
            except OSError:
                print(OSError)
