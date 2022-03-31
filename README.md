<!--  
work on comments  
add references  
-->  
# CANIS MAJORIS  
## CANSAT Project  
Hi there! This project is designed for the Can Satellite competition by AzerKosmos in Azerbaijan.  
### About the project  
The project is in form of a desktop application, which can be used to establish a connection between the host and remote satellite.  
Using this app you can:  
 - Select the COM port on the host, which will be connected to the receiver;
 - Read the data from the receiver;
 - Present the metrics in form of graph and table;
 - Send signals to the satellite (e.g. "reset")
### Installation  
Nothing special, just git clone the project, install dependancies and you are good to go!  
Run Cansat.py file to play with the application :)  

    > git clone https://github.com/gozalovash/CanSat.git
    > pip install -r requirements.txt
    > python .\Cansat.py

### Notes  
Some functions of the application contain static data just for the sake of tests without the receiver. For real cases you can always switch the functions, toggled by buttons (e.g.: self.temp_reset to self.reset).  
P.s. Just change all the toggles with "temp_" in function name.  
### Have Fun!  
Love,
Germione Granger