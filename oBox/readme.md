# Configuration of the oBox Docker containers.

New product ``oBox`` offered by One-Way Automation includes Industrial PC and suite of multiple applications. These applications are intended to connect to industrial data sources such as PLCs, harmonize and transform this data, and then forward it to various databases. 

This folder has docker compose and other accommpanying configuration files used to create and run all applications from the ``oBox`` suite as Docker containers. While mainly they are intented to run in the ``oBox Industrial PC``, they should also run in a regular Docker engine such as Docker Desktop for Windows.

Before starting containers, you will need to perform some configuration steps as descibed below.

## Adjust host names and credentials.

If you plan to access ``oBox`` suite of applications from local network only, you are free to assign host names as you wish. Resolution of host names to IP arresses should be configured using local network DNS settings or by modifying of the system file ``C:\Windows\System32\drivers\etc\hosts``.

To set custom host names, edit environment variables in the following files:

- ``.env``
- ``nginx/Dockerfile``

Note: Also edit default credentials in the file ``.env``. Do not use default values in production!

Note: in case if you plan to access oBox configuration GUI remotely from the Internet, you might need to register primary domain name with a domain registrar, and use host names as sub-domains of this primary domain. Host names for our test company composed following this approach.

## TLS certificates.

All applications are configured using web based interface. All of them except identity provider ``keycloak`` recommended to tbe accessed via reverse proxy ``nginx``, over secure https protocol. This approach simplifies certificates management, reducing number of required TLS certificates to 2: one for nginx service and one for keycloak service.

Note: steps below can look little bit cimplicated, later these steps will be automated.

## Generate TLS certificate for nginx reverse proxy server.

### Required input data.

- ``REVERSE_PROXY_HOST``: defined in file ``.env``, and in the file ``nginx/Dockerfile``. Host name of the main configuration page in the PC where oBox containers will run. For purposes of this guide lets set it to the value ``obox.testco.opcfy.io``.
-  Other fields such as common name, country, locality, organization are gereric fields used in x509 TLS certificates.
  
### Create the TLS certificate signed by OPC UA Certificate Authority.  

- Open OPC UA Registration Authority web page https://opcua.ca/ejbca/ra/

	Note: this certificate authority is used for test purposes only. For production, use your own PKI infrastructure to manage certificates. If you need help on setting up your own PKI, please contact support@onewayautomation.com.

	Note: it might ask to enter email address and then to enter a code sent to this email. In this case, first send email to support@onewayautomation.com requesting to authorize your email address to use the service. Continue to the next steps after getting approval response from One-Way Automation support.

- Click on the button ``Make New Request``
- In the field ``Certificate Type``, select option ``TLS Server Profile``
- If you have Certificate Sign Request (CSR) already generated, use option ``Provided by user``. Otherwise, select option ``By the CA``. Further below it is assumed that the later option is selected.
- Fill fields in the form. Make sure that the field DNS name is set to the same values as ``REVERSE_PROXY_HOST`` defined in file ``.env``.
- Click on button ``Download PEM``.
- Save the file in folder ``sharedFolder/nginx``.
- Open saved file in text editor.
- Copy part of the text starting from ``-----BEGIN PRIVATE KEY-----`` to the ``-----END PRIVATE KEY-----`` inclusive into clipboard.
- Open file ``nginx/own-cert/nginx-key.pem`` and replace the content with the value from clipboard, and save file.
- Go back to the file with generated certificate and copy all 3 certificates (text starting by the first ``-----BEGIN CERTIFICATE-----`` and ending by the last ``-----END CERTIFICATE-----``, inclusive).
- Open file ``nginx/own-cert/nginx-cert.pem``, replace the content with clipboard value, and save the file.
- Go back to the file with generated certificate and copy the last certificate (text starting by the last ``-----BEGIN CERTIFICATE-----`` and ending by the last ``-----END CERTIFICATE-----``, inclusive).
- Open file ``nginx/ca-certs/ca_certs.crt`` and replace content with the clipboard text, and save the file.


## Generate TLS certificate for Identity Provider service (keycloak).

The steps are similar to generating of the certificate for nginx service.

- Open OPC UA Registration Authority web page https://opcua.ca/ejbca/ra/

	Note: this certificate authority is used for test purposes only. For production, use your own PKI infrastructure to manage certificates. If you need help on setting up your own PKI, please contact support@onewayautomation.com.

	Note: it might ask to enter email address and then to enter a code sent to this email. In this case, first send email to support@onewayautomation.com requesting to authorize your email address to use the service. Continue to the next steps after getting approval response from One-Way Automation support.

- Click on the button ``Make New Request``
- In the field ``Certificate Type``, select option ``TLS Server Profile``
- If you have Certificate Sign Request (CSR) already generated, use option ``Provided by user``. Otherwise, select option ``By the CA``. Further below it is assumed that the later option is selected.
- Fill fields in the form. Make sure that the field ``DNS Name`` is set to the same values as ``KEYCLOAK_HOST`` defined in the file ``.env``.
- Click on button ``Download PEM``.
- Save the file in folder ``sharedFolder/keycloak``.
- Open saved file in text editor.
- Copy part of the text starting from ``-----BEGIN PRIVATE KEY-----`` to the ``-----END PRIVATE KEY-----`` inclusive into clipboard.
- Open file ``keycloak/certs/keycloak.pem`` and replace the content with the value from clipboard, and save file.
- Go back to the file with generated certificate and copy all 3 certificates (text starting by the first ``-----BEGIN CERTIFICATE-----`` and ending by the last ``-----END CERTIFICATE-----``, inclusive).
- Open file ``keycloak/certs/keycloak.crt``, replace the content with clipboard value, and save the file.
- Go back to the file with generated certificate and copy the last certificate (text starting by the last ``-----BEGIN CERTIFICATE-----`` and ending by the last ``-----END CERTIFICATE-----``, inclusive).
- Open file ``keycloak/certs/ca_certs.crt`` and replace content with the clipboard text, and save the file.

## Create docker-compose.yml from template file.

When used to deploy on balena OS, environment variables in the file ``docker-compose.yml`` are not substituted. For that reason, the file need to be crated using template file ``docker-compose-template.yml``, by runnign the command: 
``` 
	python.exe ./GenerateDockerCompose.py
```
As a result file ``docker-compose.yml`` will be generated from the template file, with envronment variables replaced by values from the file ``.env``.
Also, this script generates file ``grafana/grafana.ini``, with changes to run behind the reverse proxy.

## Start and configure containers

After starting containers, if this is the very first run, databases will be created and default configuration files will be created.

Once the ``keycloak`` service starts, it needs some configuration steps.
Note: default login credentials can be found in file ``.env``. 

- Click on the ``Clients`` link in the left side panel. As a result, the ``Clients`` panel will be opened in the the main screen area.
- Click on the button ``Create client``  
- In the ``Settings`` tab, fill the fields: ``Client ID``, ``Name``, ``Admin URL`` (for example, ``https://keycloak.testco.opcfy.io:8443/admin``). Turn on options ``Capability Config / Clinet Authentication`` and ``Authorization``, set ``Authentication flow`` to ``Standard``. 
- In the ``Credentials`` tab, set optoin ``Client Authenticator`` to ``Client ID and Secret``. 
- Copy value of the field ``Client Secret``. In the ``oauth2proxy`` service, set environment variable ``OAUTH2_PROXY_CLIENT_SECRET`` to this value. Also, set values of the environment variable ``OAUTH2_PROXY_CLIENT_ID``to the ``Client ID`` field from ``Settings`` tab.
- Roles assigned to the logged in users should be configured as descibed in the User Manual: https://onewayautomation.com/visual-logger-docs/html/configure.html#versions-4-0-0-or-newer
  
The service ``tunnel`` (used to access the box remotely from the Internet) needs to be configured: environment variable ``TUNNEL_TOKEN`` should be set to the value of the token from cloudflare Zero Trust tunnel settings.

## Configure DNS settings or hosts file.

Make sure that host name for the reverse proxy and keycloak service can be resolved to correct IP addresses. This can be done by DNS settsings, or by modifying file ``C:\Windows\System32\drivers\etc\hosts`` (in Windows machines).

## Trust to OPC UA CA certificates.

If browser warns that certificates are not trusted, you can downlaod OPC UA Root CA certificate and OPC UA Issuing CA Certificate from this link: ``https://opcua.ca/ejbca/ra/cas.xhtml``. And then import the root certificate into the trusred root certificates location of the OS, the second certificate - into trusted intermediate certificates location.

## Licensing of oBox applications.

The ``oBox`` suite of applications can include bunch of open source applications such as PostgreSQL or InfluxDB or Grafana or others, which do not require activation by a licence key to start using them. Meanwhile, 3 applications require activation using licenses. For evaluation, you can use free licenses, but they should be obtained from One-Way Automation and applied:

- ``DeviceGateway``, from our partner Takebishi: for free evaluation licenses, as well as for production licenses, please contact sales@onewayautomation.com, or send a message using online form https://onewayautomation.com/contact-us . 
- ``ogamma Visual Logegr for OPC``: you can get a free evaluation license for it at our online store: https://onewayautomation.com/online-store#. Activation of this application is described in online User Manual: https://onewayautomation.com/visual-logger-docs/html/activate.html#activate
- ``ProsysOPC UA Forge``, from our partner ProsysOPC: for free evaluation licenses, as well as for production licenses, please contact sales@onewayautomation.com, or send a message using online form https://onewayautomation.com/contact-us .