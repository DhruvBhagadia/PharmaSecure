# PharmaSecure
PharmaSecure is an application that provides a secured, homomorphic way of storing crucial, sensitive pharmaceutical data on the cloud. It is an application that we implemented as our final year project for Bachelor's Degree in Computer Engineering.

Our research is published in [Web Of Science journal](http://sersc.org/journals/index.php/IJFGCN/article/view/17887) and has received the [Best paper award](https://photos.app.goo.gl/hmBGN9uLPGHXrnqC8) at ICCTAW conference (Computing technologies for Transforming the Automated World) held in April 2020

## Homomorphic Encryption
Homomorphic Encryption is an encryption technique that allows specific computations on
data in its encrypted form (cipher texts). The result is always encrypted data (cipher text),
which results from operations performed on encrypted data of plain text. Homomorphic
Encryption provides the basis of manipulating data without decrypting it first. We make use of **Paillier Homomorphic Encryption scheme** in our implementation.

## Key Storage on the Server
Our application focuses on two users, managers and researchers/employees. In any case the
keys need to be stored securely on the servers. There are various ways that we explored and
then came to a conclusion of making use of the most suitable one. Few methods are:

### HSM (Hardware Security Module)
It is a separate hardware module in which sensitive keys are stored. The major advantage that
this method provides is it’s distal from the actual server. The keys are stored on the HSM and
never leaves the appliance un-encrypted. Any cryptographic activity that involves the private
key is carried out internally within the device. However, considering the overhead of extra
hardware we didn’t opt for this option in our project.

### Encrypted file with key supplied on runtime
This method provides additional layers of security with protection against offline attacks.
This method requires the user to supply the secret key used to encrypt files containing
cryptographic keys before using it. Here the secret is already shared with the user while
registering with the system, he has to use the same secret in the future to fetch cryptographic
keys.

### Encrypted file with hidden key
Another solution for securely storing keys on the server is to store it in a particular file and
then encrypting that file with the user password or equivalent key. The major advantages
provided by such a service is getting more control while logging into the system to get results. We make use of this technique thereby securing the storage of keys on the server.

Here is how the file storing key looks:
![pasted image 0](https://user-images.githubusercontent.com/32220881/84137288-17c0fb80-aa6a-11ea-9310-625f06955d52.png)

## Methodology
* The two primary users of our application are *Manager* and *Researcher* present in pharmaceutical industries.
* Employees/Researchers perform the work of experimentation while developing medicine, because of which there are frequent changes to the quantities of the components present in the medicines. 
* These pieces of information are very confidential and hence should be visible to only authorized people like the manager. The manager holds all the rights like adding/removing employees, watching detailed descriptions of medicines, etc.
* All the keys used for cryptographic operations are stored securely (encrypted form) on the servers adding an extra bit of security to the application.

## Flowcharts
![image](https://user-images.githubusercontent.com/32220881/84137806-d41ac180-aa6a-11ea-9314-3181ff164a06.png) ![image](https://user-images.githubusercontent.com/32220881/84137862-edbc0900-aa6a-11ea-8db0-737a11dc8206.png)

## Screenshot 
#### Database entry of Medicine components

![image](https://user-images.githubusercontent.com/32220881/84143326-02e96580-aa74-11ea-89ac-6b58cbf207de.png)

## Demo
Here is the demo of our app in form of gifs.


![1](https://user-images.githubusercontent.com/32220881/84142462-725e5580-aa72-11ea-9406-181c49e3c549.gif)
------------------------------------------------------------------------------------------
![2](https://user-images.githubusercontent.com/32220881/84142604-b3566a00-aa72-11ea-839a-6ccf0f041d43.gif)
--------------------
![3](https://user-images.githubusercontent.com/32220881/84142673-d3862900-aa72-11ea-838f-9274154067bc.gif)
-------------
![4](https://user-images.githubusercontent.com/32220881/84142713-e7ca2600-aa72-11ea-970e-1a2c23be6b79.gif)
-------------

### Made by team DJ Hackers
* [Dhruv Bhagadia](https://github.com/DhruvBhagadia)
* [Devansh Dalal](https://github.com/da2ash)
* [Mustafa Bhanpurawala](https://github.com/mustafabhanpura)

#### Feedbacks are welcome
