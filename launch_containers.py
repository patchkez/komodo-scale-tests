#!/usr/bin/env python3
import docker
import pprint
import sys
from chains_config import *

pp = pprint.PrettyPrinter(indent=1)
client = docker.from_env()
chains_array = chains_array_test # debug

arg = ''
try:
  arg = sys.argv[1]
except:
  pass

# treat arguments
if arg == 'stop':
  for index, coin in enumerate(chains_array):
    coin_name = coin[0]
    container_name = coin_name
    try:
      container = client.containers.get(container_name)
      container.stop()
      print("Stopping container " + container.name)
    except Exception as e:
      print(e)
  exit(0)
elif arg == '':
  pass
else:
  print("Argument not recognized.")
  exit(1)

# launch container instances
for index, coin in enumerate(chains_array):
  coin_name = coin[0]
  coin_port = coin[1]
  coin_p2p_port = int(coin_port) - 1
  container_name = coin_name
  # persistent volume if needed
  if persistent_volumes is True:
    target = "/home/komodo/.komodo"
    source = "komodo_tests_" + container_name 
    mount_volumes = [docker.types.Mount(target, source)]
  else:
    mount_volume = ''
  # port sharing if needed
  if share_p2p is True:
    ports_sharing = {str(coin_p2p_port) + '/tcp': ('0.0.0.0', coin_p2p_port)}
  else:
    ports_sharing = ''
  if mining is True:
    gen = "-gen"
  else:
    gen = ""
  # build command string
  commandstr = (
    " " + gen +
    " -addnode=" + container_name + " " +
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


