from netmiko import ConnectHandler
import datetime

# Define the FortiGate devices details
devices = [   
{
    'device_type': 'fortinet',
    'ip': '10.108.3.145',
    'host': 'NGOLA',
    'username': 'ECN01_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
},

{
    'device_type': 'fortinet',
    'ip': '172.30.104.14',
    'host': 'ANGOLA-DC',
    'username': 'evabssi_EU_mco',
    'password': 'P299[q;dp+FC'
    
},

{
    'device_type': 'fortinet',
    'ip': '10.105.21.1',
    'host': 'NOCAL',
    'username': 'NOC_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
},

{
    'device_type': 'fortinet',
    'ip': '10.107.35.201',
    'host': 'SOBA',
    'username': 'SBA_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
},
{
    'device_type': 'fortinet',
    'ip': '10.105.3.209',
    'host': 'FUNDA',
    'username': 'CBL_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
},

{
    'device_type': 'fortinet',
    'ip': '10.106.3.217',
    'host': 'COBEJE',
    'username': 'CBJ_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
},

{
    'device_type': 'fortinet',
    'ip': '10.107.18.89',
    'host': 'NOCEBO',
    'username': 'NCB_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
},

{
    'device_type': 'fortinet',
    'ip': '10.107.4.57',
    'host': 'VIDRUL',
    'username': 'VID_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
},
{
    'device_type': 'fortinet',
    'ip': '10.107.58.57',
    'host': 'SOCOMIA',
    'username': 'SOC_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
},
{
    'device_type': 'fortinet',
    'ip': '10.107.49.25',
    'host': 'CERBAB',
    'username': 'CRB_EVABSSI_EU_MCO',
    'password': 'Fdf04154!ffdA'
    
}


]
# Get the current date
date = datetime.datetime.now().strftime('%Y-%m-%d')

for device in devices:

# Connect to the FortiGate device
    net_connect = ConnectHandler(**device)

# Enter into configuration mode
    net_connect.config_mode()

# Save the full configuration to a file
    print('SSH Connection to ' + device['host'] + ' is successful')
    output = net_connect.send_command('show full-configuration', read_timeout=60)
    with open(device['ip'] + '_' + date + '_config.txt', 'w') as file:
        file.write(output)

# Backup status
    print('Backup of ' + device['host'] + ' is successful')

    # Disconnect from the device
    net_connect.exit_config_mode()
    net_connect.disconnect()