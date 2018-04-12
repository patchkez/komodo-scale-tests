# komodo-scale-tests
Testing new komodo scaling capabilities.

### Install Docker CE for your platform
Follow official installation instructions, e.g. for Ubuntu:
https://docs.docker.com/install/linux/docker-ce/ubuntu/
Make sure your user is member of docker group, so you can execute docker cli commands as user:
```
sudo useradd -G docker <user>
```

### Build komodod image (optional)
This step is optional, @emmanux build Docker image and pushed it to Dockerhub. Upon first start of the script,
image will be downloaded automatically for you from Dockerhub.

Clone the repository with Dockerfiles (these are definitions files how Docker images will be build):
```
cd projects
git clone https://github.com/Emmanux/kmdplatform
```
Build docker image:
```
cd kmdplatform/komodod
docker build --build-arg KOMODO_BRANCH=jl777 . -t kmdplatform/komodod:jl777
```

### Docker network
Create docker network, all our test containers will use it:
```
docker network create dockernet
```

### Install python virtualenv
Install needed packages:
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
```
Create virtualenv:
```
virtualenv komodo-scale-venv
```
Activate the environment:
```
source komodo-scale-venv/bin/activate
```

Install needed python packages:
```
pip install docker
```

### launch_containers.py usage:
Clone this repository
```
cd projects
git clone https://github.com/Emmanux/komodo-scale-tests
cd komodo-scale-tests
```

First of all, review the configuration file "chains_config.py", it is read at each run.

`./launch_containers.py` – starts batch of instances with id 1

`./launch_containers.py start` – same as above

`./launch_containers.py start 1` – same as above

`./launch_containers.py start 2` – starts batch of instances with id 2

`./launch_containers.py stop 2` – stops batch of instances with id 2
