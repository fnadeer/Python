from netmiko import ConnectHandler
import datetime
import pandas as pd

# Load the Excel file with the FortiGate device details and credentials
devices_df = pd.read_excel('fortigate_devices_test.xlsx')

# Get the current date
date = datetime.datetime.now().strftime('%Y-%m-%d')

# Loop through each FortiGate device and save the full configuration to a file
for index, row in devices_df.iterrows():
    # Define the FortiGate device details
        device = {
            'device_type': 'fortinet',
            'ip': row['IP Address'],
            'username': row['Username'],
            'password': row['Password']
        }

    # Connect to the FortiGate device
        net_connect = ConnectHandler(**device)

    # Enter into configuration mode
        net_connect.config_mode()


    # Save the full configuration to a file
        print('SSH Connection to ' + row['Hostname'] + ' is successful')
        output = net_connect.send_command('show full-configuration', read_timeout=60)
        with open(row['Hostname'] + '_' + date + '_config.conf', 'w') as file:
            file.write(output)
    # Backup status
        print('Backup of ' + row['Hostname'] + ' is successful')

    # Disconnect from the device
        net_connect.exit_config_mode()
        net_connect.disconnect()
