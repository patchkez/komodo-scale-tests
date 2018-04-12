#!/usr/bin/env python3
import docker
import pprint
import sys
# from .chains_config import *
from chains_config import chains_array_test, pubkey, rpcuser, rpcpassword, share_p2p, \
    persistent_volumes, mining, seed_node, chains_array

# initialize things
pp = pprint.PrettyPrinter(indent=1)
client = docker.from_env()
chains_array = chains_array_test  # debug


def launch_containers(batch_id):
    try:
        batch_id = "_" + batch_id
    except:
        batch_id = ""
    # iterate coin list
    for index, coin in enumerate(chains_array):
        coin_name = coin[0]
        coin_port = coin[1]
        coin_p2p_port = int(coin_port) - 1
        container_name = coin_name + batch_id
        # persistent volume if needed
        if persistent_volumes is True:
            target = "/home/komodo/.komodo"
            source = "komodo_tests_" + container_name
            mount_volumes = [docker.types.Mount(target, source)]
        else:
            mount_volumes = ''
        # port sharing if needed
        if share_p2p is True and batch_id == 1:
            ports_sharing = {
                str(coin_p2p_port) + '/tcp': ('0.0.0.0', coin_p2p_port)}
        else:
            ports_sharing = ''
        # mining if needed
        if mining is True:
            gen = "-gen"
        else:
            gen = ""
        # seed node if specified
        try:
            seednode = seed_node
        except:
            seednode = coin_name + '_1'
        # build command string
        commandstr = (
            "komodod" +
            " " + gen + " " +
            "-addnode=" + seednode + " " +
            "-pubkey=" + pubkey + " " +
            "-rpcallowip=0.0.0.0/0 " +
            "-rpcuser=" + rpcuser + " " +
            "-rpcpassword=" + rpcpassword + " " +
            "-ac_name=" + coin_name + " " +
            "-ac_supply=1000000 " +
            "-ac_end=0 -ac_reward=0 -ac_halving=0 -ac_decay=0"
        )
        # run container
        container = client.containers.run(
            "kmdplatform/komodod:jl777",
            detach=True,
            remove=True,
            network="dockernet",
            name=container_name,
            command=commandstr,
            ports=ports_sharing,
            mounts=mount_volumes
        )
        pp.pprint(container)


def stop_containers(batch_id):
    try:
        batch_id = "_" + batch_id
    except:
        batch_id = ""
    # iterate coin list
    for index, coin in enumerate(chains_array):
        coin_name = coin[0]
        container_name = coin_name + batch_id
        try:
            container = client.containers.get(container_name)
            container.stop()
            print("Stopping container " + container.name)
        except Exception as e:
            print(e)
    exit(0)


def main():
    # treat arguments
    arg1 = ''
    try:
        arg1 = sys.argv[1]
    except:
        pass
    batch_id = '1'
    try:
        batch_id = sys.argv[2]
    except:
        pass
    # define arguments logic
    if arg1 == 'start' or arg1 == '':
        launch_containers(batch_id)
    elif arg1 == 'stop':
        stop_containers(batch_id)
    else:
        print("Argument not recognized.")
        exit(1)


if __name__ == "__main__":
    main()
