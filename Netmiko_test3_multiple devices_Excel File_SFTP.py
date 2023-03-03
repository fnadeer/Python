from netmiko import ConnectHandler
import datetime
import pandas as pd
import paramiko

# Load the Excel file with the FortiGate device details and credentials
devices_df = pd.read_excel('fortigate_devices.xlsx')

# Define the SFTP server details
sftp_server = '192.168.0.23'
sftp_port = 2222
sftp_username = 'tester'
sftp_password = 'password'
sftp_directory = 'C:/Users/fnadeer/Downloads/RebexTinySftpServer-Binaries-Latest/data'



# Create an SFTP transport
transport = paramiko.Transport((sftp_server, sftp_port))
transport.connect(username=sftp_username, password=sftp_password)

# Create an SFTP client
sftp_client = paramiko.SFTPClient.from_transport(transport)

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
    filename = row['Hostname'] + '_' + date + '_config.conf'
    with open(filename, 'w') as file:
        file.write(output)

    # Backup status
    print('Backup of ' + row['Hostname'] + ' is successful')

    # Disconnect from the device
    net_connect.exit_config_mode()
    net_connect.disconnect()

    # Upload the configuration file to SFTP server
    try:
        sftp_client.put(filename, sftp_directory + '/' + filename)
        print('Upload of ' + filename + ' to SFTP server ' + sftp_server + ' is successful')
    except Exception as e:
        print('Upload of ' + filename + ' to SFTP server ' + sftp_server + ' failed with error: ' + str(e))

# Close the SFTP client and transport
sftp_client.close()
transport.close()
