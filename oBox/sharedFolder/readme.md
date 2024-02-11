Content of this folder can be shared between all docker containers. It has sub-folders for containers. At provisioing stage, some initialization files can be put in these folders. One purpose is to save generated TLS and / or OPC UA application instance certificates. Also, common PKI files can be stored there, for example, CA certificates.
For security reasones, private keys should not be stored there. 

Exchange with files can be done by creating files with predefined name in one container, and detect its creation in another container and react to that event accordingly. Detection of new files and reaction to those events can be done in bash script files running in background.

For example, workflow of updating of the TLS certificate for nginx can be as follows below. The Main Portal Applicatoin (or Manager Application) here is some web application which can be created later, serving as entry point for the whole solution. In case with oBox, it is expected to be the main configuration page.

1. Generate certificate sign request, sign it with CA, and update nginx container with it.

	- Manager Application creates file in sharedFolder/nginx/createCsr.req
	- Background script in nginx container 
		- detects creating of this file
		- creates CSR file nginx.csr
		- deletes file nginx/createCsr.req
		- creates file createCsr.res. It can have result of executing the command: OK in case of success, or error message in case of failure.
	- Manager Application:
		- detects that file nginx/createCsr.res is created. 
		- It takes the file nginx/nginx.csr, connects to the PKI RA (registration authority), and signs it.
		- Puts signed certificate in folder nginx/signedCert.pem
		- Optionally, can put file nginx/privateKey.pem with private key. To force sugin of this file, additional file needs to be created: provisioing.req
			Note: these 2 files can be created manually before starting of containers. 
		- Creates file nginx/updateCert.req
		
	- Background script in nginx container:
		- detects that file updateCert.req is created
		- verifies that file nginx/signedCert.pem is valid
		- moves this file to its PLS certificate folder.
		- deletes file nginx/updateCert.req
		- creates response  file nginx/updateCert.res
		- restarts
	- Manager application:
		- detecs that file nginx/updateCert.res is created.
		- reports in the GUI that operation succeeded or failed.
		
2. Providing security. 
	In the future, in the request / response files we can save JWT token, with some predefined roles authorizing participating applications.
	
	
3. Provisioning. 

Signing of the initial TLS certificate after provisioing of the new device can be done this way.

	1. Background script in the container (nginx) detects that there is no certificate file. It should:
		- create private key file
		- generate CSR and create file nginx/createCsr.res
		- This will be processed by the main application and signed certificate will be created.
		- 
	2. Alternatively, as a quick temporary solution, we can generate both private key and certificate file, and create file nginx/provisioning.req. All the background script needs to do is to detect that file nginx/provisioning.req exists, mode certificate files and remove file nginx/provisioning.req
	

