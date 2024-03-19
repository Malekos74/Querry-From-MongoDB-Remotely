from paramiko.client import SSHClient

# SSH tunnel parameters (Can be changed accordingly)
SSH_HOST = 'YOUR HOST IP'
SSH_USER = 'YOUR USERNAME'
SSH_PASSWORD = 'YOUR PASSWORD'
SSH_PORT =  22  # Default SSH port

client = SSHClient()
client.load_system_host_keys()

try:
    client.connect(SSH_HOST, #port = SSH_PORT,
                             username = SSH_USER,
                             password = SSH_PASSWORD,
                             look_for_keys = False)
    print("Connected successfully!")
    
    # CMD ='''echo "Executing Bash script..."
    #         echo "Current directory: $(pwd)"
    #         echo "List of files:"
    #         ls -l
    #         echo "System information:"
    #         uname -a'''
    CMD ='''echo "Hello" '''
    stdin, stdout, stderr = client.exec_command(CMD)
    
    output = stdout.readlines()
    
    with open("backup2.txt", "w") as out_file:
        for line in output:
            out_file.write(line)
            
    for line in output:
        print(line.strip()) 
    
    
    client.close()
except Exception:
    print("Failed to establish connection.")
finally:
    client.close()