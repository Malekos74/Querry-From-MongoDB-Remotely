"""
    Python program that helps you connect to a specified mongoDB on a remote server.
        
    INPUT:
        - Database name (Default value: CHP)                 | Input through
        - Collection name (Default value: characterization)  | Code parameters
        - Timestep (input through STDIN)
    OUTPUT:
        - All objects that have the timestep inputted
    
    NB:
        - You need to be connected to the Uni network for the SSH connection to work (Or use eduVPN)
        - Input float should be with a '.' and not a ','
        - If the following error message appears when querrying: "No row exists with the specified timestep None",
          then the conversion of the input into float failed. Please check the timestep and try again.
        - If the program times out at any point, please try again.
        
[Malek Miled] 19.03.2024
"""
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder

# SSH tunnel parameters (Can be changed accordingly)
SSH_HOST = 'YOUR HOST IP'
SSH_USER = 'YOUR USERNAME'
SSH_PASSWORD = 'YOUR PASSWORD'
SSH_PORT =  22  # Default SSH port

# MongoDB parameters (Can be changed accordingly)
MONGO_HOST = '127.0.0.1'  # This points to localhost because MongoDB will be accessed through the SSH tunnel
MONGO_PORT =  27017
# Specify the needed DB and COLLECTION as you see fit
DB = 'CHP'
COLLECTION = 'characterization'


# Extracts values out of the querried value
def extractValues(list):
    return [list[0]['P'], list[0]['Q'], list[0]['P_ref']]

# Prints a list with the number of objects printed
def printList(list):
    print("\n")
    for x in list:
        print(x)
    print("\nPrinted ", len(list), " Objects.")

# Querries from the specified DB and collection based on an inputted timestep. Returns a list of the form:
# [documents, P, Q, P_ref, timestep] with documents being a list of dictionaries. Each dictionary represents an object
# that exist in that DB and collection and has a Time [s] value of timestep. 
def querry(db , collection, timestep = -1):  
    # Documentation on how to build complex querries: https://www.w3schools.com/python/python_mongodb_query.asp
    
    # Access the current database
    current_db_name = db.name
    print("\nCurrent database:", current_db_name)
    # Correctly print the current collection
    print("Current collection:", COLLECTION, "\n")
    
    # Fetch all documents from the collection (Empty list if no row exists for the specified timestep)
    documents = list(collection.find({'Time [s]': timestep}))
    
    if len(documents) == 0:
        print("No row exists with the specified timestep: ", timestep)
        # printList(list(collection.find()))
        return None
    
    return documents

# Prints all timesteps of the given collection in the given DB that are not NA
def printAllTimesteps(db , collection):
     # Access the current database
    current_db_name = db.name
    print("\nCurrent database:", current_db_name)
    # Correctly print the current collection
    print("Current collection:", COLLECTION, "\n")
    
    # Fetch all documents from the collection (Empty list if no row exists for the specified timestep)
    documents = list(collection.find())
    
    # Assuming documents is a list of dictionaries
    time_values = [doc.get('Time [s]', None) for doc in documents]
    # Filtering out None values if any
    time_values = [value for value in time_values if value is not None]
    # Sort time_values
    time_values.sort()

    # Printing the list of time values
    print(time_values)
    
# Extracting the values takes into consideration that the result of the querry
# will always be a list of length 1 since time values are unique
if __name__ == '__main__':
    try:
        # Connect to MongoDB through the SSH tunnel
        with SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),   
            ssh_username = SSH_USER,
            ssh_password = SSH_PASSWORD,
            remote_bind_address = ('127.0.0.1', MONGO_PORT)
        ) as tunnel:

            client = MongoClient(MONGO_HOST, tunnel.local_bind_port)
            db = client[DB]
            collection = db[COLLECTION]
            
            # Specify a Timestep. None if the conversion fails.
            try:
                timestep = float(input("Input the wanted timestep: "))
            except ValueError:
                timestep = None

            
            # Querry based on the specified values
            result = querry(db, collection, timestep)
            
            
            if result is not None:
                # Prints the querried values on STDOUT
                printList(result)
                
                # Initialize all needed variables for later use
                [P, Q, P_ref] = extractValues(result)  
                # print(P)
                # print(Q)
                # print(P_ref)
            else:
                print("Rerun the code and input an existing timestep.")
                
            # printAllTimesteps(db, collection)
                
             
    except Exception as e:
        print("An error occurred:", e)
