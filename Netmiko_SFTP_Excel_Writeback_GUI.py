from tkinter import *
from tkinter import filedialog
import pandas as pd
import datetime
import paramiko
from netmiko import ConnectHandler

# Define the main function to run the script
def run_script():
    # Load the Excel file with the FortiGate device details and credentials
    devices_df = pd.read_excel(file_path.get())

    # Define the SFTP server details
    sftp_server = sftp_server_entry.get()
    sftp_port = sftp_port_entry.get()
    sftp_username = sftp_username_entry.get()
    sftp_password = sftp_password_entry.get()
    sftp_directory = sftp_directory_entry.get()

    # Create an SFTP transport
    transport = paramiko.Transport((sftp_server, int(sftp_port)))
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
        output = net_connect.send_command('show full-configuration', read_timeout=60)
        filename = row['Hostname'] + '_' + date + '_config.conf'
        with open(filename, 'w') as file:
            file.write(output)

        # Backup status
        print('Backup of ' + row['Hostname'] + ' is successful')

        # Disconnect from the device
        net_connect.exit_config_mode()
        net_connect.disconnect()

        # Define the cell to write the backup status to
        status_cell = 'C' + str(index + 2)  # Assumes device details start on row 2

        # Write the backup status to the Excel file
        try:
            sftp_client.put(filename, sftp_directory + '/' + filename)
            devices_df.at[index, 'Backup Status'] = 'Success'
            print('Upload of ' + filename + ' to SFTP server ' + sftp_server + ' is successful')
        except Exception as e:
            devices_df.at[index, 'Backup Status'] = 'Failed: ' + str(e)
            print('Upload of ' + filename + ' to SFTP server ' + sftp_server + ' failed with error: ' + str(e))
            file = ''
        # Save the updated Excel file
        devices_df.to_excel(file_path.get(), index=False)

    # Close the SFTP client and transport
    sftp_client.close()
    transport.close()

# Define the function to browse for the Excel file
def browse_file():
    file_path.set(filedialog.askopenfilename())

# Create the main window
root = Tk()
root.title("FortiGate Backup Tool")

# Create the frame for the input fields
input_frame = Frame(root)
input_frame.pack()

# Add the Excel file input field and browse button
file_path = StringVar()
file_label = Label(input_frame, text="Excel File:")
file_entry = Entry(input_frame, textvariable=file_path)
file_entry.pack(side=LEFT, padx=5, pady=5)

browse_button = Button(input_frame, text="Browse", command=browse_file)
browse_button.pack(side=LEFT, padx=5, pady=5)

sftp_server_label = Label(input_frame, text="SFTP Server:")
sftp_server_entry = Entry(input_frame)
sftp_server_label.pack(side=LEFT, padx=5, pady=5)
sftp_server_entry.pack(side=LEFT, padx=5, pady=5)

sftp_port_label = Label(input_frame, text="SFTP Port:")
sftp_port_entry = Entry(input_frame)
sftp_port_label.pack(side=LEFT, padx=5, pady=5)
sftp_port_entry.pack(side=LEFT, padx=5, pady=5)

sftp_username_label = Label(input_frame, text="SFTP Username:")
sftp_username_entry = Entry(input_frame)
sftp_username_label.pack(side=LEFT, padx=5, pady=5)
sftp_username_entry.pack(side=LEFT, padx=5, pady=5)

sftp_password_label = Label(input_frame, text="SFTP Password:")
sftp_password_entry = Entry(input_frame, show="*")
sftp_password_label.pack(side=LEFT, padx=5, pady=5)
sftp_password_entry.pack(side=LEFT, padx=5, pady=5)

sftp_directory_label = Label(input_frame, text="SFTP Directory:")
sftp_directory_entry = Entry(input_frame)
sftp_directory_label.pack(side=LEFT, padx=5, pady=5)
sftp_directory_entry.pack(side=LEFT, padx=5, pady=5)

run_button = Button(root, text="Run Backup", command=run_script)
run_button.pack(pady=10)

root.mainloop()