# komodo-scale-tests
Testing new komodo scaling capabilities.

### launch_containers.py usage:

First of all, review the configuration file "chains_config.py", it is read at each run.

`./launch_containers.py` – starts batch of instances with id 1

`./launch_containers.py start` – same as above

`./launch_containers.py start 1` – same as above

`./launch_containers.py start 2` – starts batch of instances with id 2

`./launch_containers.py stop 2` – stops batch of instances with id 2
