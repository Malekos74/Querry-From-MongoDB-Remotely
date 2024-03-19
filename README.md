# Python program that helps you connect to a specified mongoDB on a remote server.
    
### INPUT:
    - Database name (Default value: CHP)                 | Input through
    - Collection name (Default value: characterization)  | Code parameters
    - Timestep (input through STDIN)
### OUTPUT:
    - All objects that have the timestep inputted

### NB:
    - You need to be connected to the Uni network for the SSH connection to work (Or use eduVPN)
    - Input float should be with a '.' and not a ','
    - If the following error message appears when querrying: "No row exists with the specified timestep None",
      then the conversion of the input into float failed. Please check the timestep and try again.
    - If the program times out at any point, please try again.
        
[Malek Miled] 19.03.2024
