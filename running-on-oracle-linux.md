# Installing and running ogamma Visual Logger for OPC on Oracle Linux v 8.2

## Install and run Docker engine (Podman).

### Update the system, enable developer repository, enable and start docker, as described here:

https://docs.oracle.com/en/learn/ol-podman-compose/index.html

In our test setup commands below were run:

```
sudo yum update -y

sudo yum install -y oraclelinux-developer-release-el8
sudo yum config-manager --enable ol8_developer

sudo yum install -y docker
sudo systemctl enable podman --now
sudo systemctl start podman
sudo systemctl status podman  # verify it is running

sudo curl -SL https://github.com/docker/compose/releases/download/v2.28.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

systemctl --user enable --now podman.socket
systemctl --user status podman.socket

sudo dnf install -y oracle-epel-release-el8
sudo dnf config-manager --enable ol8_developer_EPEL

sudo dnf install -y podman-compose 
```

### Download docker-compose.yml file for OVL


```
mkdir docker\ovl
cd docker\ovl

wget https://onewayautomation.com/docker/ovl/docker-compose.yml
```

### Optional: edit docker-compose.yml file

The docker compose configuration file has 2 services: one for OVL, and second for Macchina Remote Agent. The second service can be used to access OVL configuration remotely, from the Internet. For details about this product refer this page: https://macchina.io/remote.html

To sign-up for trial version of the service, visit https://remote.macchina.io/my-devices/signup

After sign-in to the service, login at https://remote.macchina.io/my-devices/login Then add new device, and update environment variables in the docker-compose.yml file with values from Macchina service page:

  - WEBTUNNEL_DOMAIN
  - WEBTUNNEL_DEVICE_ID
  - WEBTUNNEL_DEVICE_NAME

Now start containers:

```
sudo podman-compose up -d
```

The OVL configuration GUI will be available at port 4880 of the host machine. Default credentials are ``admin/password``. To access the GUI remotely, on Macchina page click on the link with device name.

For further steps on configuration of the OVL, please refer online User Manual at https://onewayautomation.com/visual-logger-docs/html/

Short getting started information also can be found on the main panel of the configuration page.

Note that remote access can also be set up using other solutions. Also, it is possible to run the OVL behind of reverse proxy and with user authentication integrated by external oAuth identity provider. For more information please contact support@onewayautomation.com
