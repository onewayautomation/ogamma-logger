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

## Download docker-compose.yml file for OVL

If you are using this repository, the file can be found at this path relative to the repository root folder: ``docker/oracle-linux/docker-compose.yml``.

It can be also downloaded by the command:

```
wget https://github.com/onewayautomation/ogamma-logger/blob/master/docker/oracle-linux/docker-compose.yml
```

### Optional: edit docker-compose.yml file

The docker compose configuration file has 2 services: one for OVL, and second, optional, is for Macchina Remote Agent.
 
Review and change as needed settings for the service ``ogamma-logger``.

If not required/applicable, comment or remove the second service lines from the file ``docker-compose.yml``.

#### About Macchina Remote Agent.

The Macchina Remote Agent service is optional, can be used to access OVL configuration GUI remotely, from the Internet. Disable it if there is no outgoing traffic enabled in the Docker host machine where the OVL will run, or if you don't need access from the Internet. For details about this product refer its home page at https://macchina.io/remote.html

To sign-up for free trial version of the Machchina Remote Agent service, visit https://remote.macchina.io/my-devices/signup

After sign-in to the service, login at https://remote.macchina.io/my-devices/login Then add new device, and update environment variables in the docker-compose.yml file with values from Macchina service page:

  - WEBTUNNEL_DOMAIN
  - WEBTUNNEL_DEVICE_ID
  - WEBTUNNEL_DEVICE_NAME

## Special case: offline setup.

This section is applicable for the case when the Docker host has no access to the Internet to download file ``docker-compose.yml`` and Docker images.

- In the host that has access to the Internet, download files from our website:

  - File ``docker-compose.yml``: https://github.com/onewayautomation/ogamma-logger/blob/master/docker/oracle-linux/docker-compose.yml
  - Create OVL Docker image file using the script below. It pulls the image from Docker Hub and packages it into archive file ``ovl-latest.tar.gz``:

    ```
    #!/bin/sh
    # This script pulls docker image of the OVL (ogamma/logger) from Docker Hub and saves it in .tar.gz file.
    imageName=ogamma/logger:latest
    fileName=ovl-latest.tar.gz
    echo "Pulling image $imageName from Doker Hub ..."
    docker pull docker.io/$imageName
    if [ $? == 0 ]; then
      echo "Saving image $imageName in archive file $fileName..."
      docker save $imageName | gzip -9 > $fileName
      if [ $? == 0 ]; then
        echo "Done"
        echo "To load the image from file $fileName on another machine offline, run the command:"
        echo "gunzip -c $fileName | docker load"
      else
        echo "Failed to save the image $imageName in file $fileName"
        exit 2
      fi
    else
      echo " Failed to pull the image $imageName"
     exit 1
    fi
    ```

  Copy the script content and save it in file ``download-docker-image.sh``, change file mode to executable, and run it.

  Alternatively, download the script file and run it using commands:
  
  ```
  wget https://onewayautomation.com/docker/ovl/download-docker-image.sh
  chmod +x download-docker-image.sh
  ./download-docker-image.sh
  ```

- Then copy these 2 files to the Docker host (which if offline):

  - ``ovl-latest.tar.gz``
  - ``docker-compose.yml``

- To load the container image from file in the Docker host, run the command:

  ```
  gunzip -c $fileName | docker load
  ```

Now the OVL image is ready to start it in a Docker container. 


## Start containers:

Navigate to the folder with file ``docker-compose.yml`` and run the command:

```
sudo podman-compose up -d
```

The OVL configuration GUI will be available at http port 4880 of the host machine. Default credentials are ``admin/password``. 

Optional if the Macchina Reote agent is enabled: to access the GUI remotely, on Macchina page click on the link with device name.

For further steps on configuration of the OVL, please refer online User Manual at https://onewayautomation.com/visual-logger-docs/html/

Short getting started information also can be found on the main panel of the configuration page.

Note that remote access can also be set up using other solutions. Also, it is possible to run the OVL behind of reverse proxy and with user authentication integrated by external oAuth identity provider. For more information please contact support@onewayautomation.com
