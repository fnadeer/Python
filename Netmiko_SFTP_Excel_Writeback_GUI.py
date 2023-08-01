import paramiko
import time
import datetime
import pandas as pd

# Load the input data from an Excel file
data = pd.read_excel('fortigate_devices_Production3.xlsx')

# Create an empty list to store the hostnames of firewalls where the SSH connection fails
failed_connections = []
failed_sftp = []

for index, row in data.iterrows():
    # Extract the IP address, username, and password for the FortiGate firewall from the current row of data
    ip_address = row['IP Address']
    username = row['Username']
    password = row['Password']
    hostname = row['Hostname']

    # Get the current date and time to use in the backup config file name
    now = datetime.datetime.now()
    backup_file_name = f"{hostname}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.conf"

    # Set the command to execute on the firewall with the new backup config file name
    command = f'execute backup config sftp {backup_file_name} 10.246.208.167  <put your username and password of your sftp server here>'

    # Create a new SSH client and set the policy to use the default system policy
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the FortiGate firewall using SSH
        ssh.connect(ip_address, username=username, password=password)
        print('SSH Connection to ' + row['Hostname'] + ' Successful')

        # Start an interactive shell session
        channel = ssh.invoke_shell()

        # Enter into the config global mode
        channel.send('config global\n')

        # Wait for the prompt to change to "(global)" indicating that we are in the config global mode
        while not channel.recv_ready():
            pass       
        output = channel.recv(1024).decode('utf-8')
        print(output)

        # Execute the command and store the output
        channel.send(command + '\n')
        time.sleep(20)
        while not channel.recv_ready():
            pass
        output = channel.recv(1024).decode('utf-8')
        print(output)
        # Check if the backup config file was successfully sent to the SFTP server
        if 'failed' in output:
            failed_sftp.append(hostname)

    except Exception as e:
        print(f"Failed to connect to {hostname} with IP {ip_address}: {str(e)}")
        failed_connections.append(hostname)

    finally:
        # Close the SSH connection
        ssh.close()

# Print the list of hostnames of firewalls where the SSH connection failed
if failed_connections:
    print(f"\nFailed to connect to the following {len(failed_connections)} firewall(s):")
    for hostname in failed_connections:
        print(hostname)

else:
    print("\nAll SSH connections successful.")

if failed_sftp:
    print(f"\nFailed to send backup config file to the SFTP server for {len(failed_sftp)} firewall(s):")
    for hostname in failed_sftp:
        print(hostname)
else:
    print("\nAll backup config files were sent to the SFTP server successfully.")
