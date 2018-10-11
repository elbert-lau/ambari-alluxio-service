#!/usr/bin/config python
from resource_management import *
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.version import compare_versions, format_hdp_stack_version
from resource_management.libraries.functions.format import format

import commands
import os.path

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

# identify archive file
alluxio_archive_file = 'alluxio-1.6.1-hadoop-2.7-bin.tar.gz'

#config['configurations']['alluxio-env']['alluxio.archive.file']

# alluxio masters address
alluxio_masters = config['clusterHostInfo']['alluxio_master_hosts']
alluxio_masters_str = '\n'.join(alluxio_masters)

# alluxio workers address
alluxio_workers = config['clusterHostInfo']['alluxio_slave_hosts']
alluxio_workers_str = '\n'.join(alluxio_workers)

# alluxio underfs address
underfs_addr = config['configurations']['alluxio-env']['alluxio.underfs.address']

# alluxio worker memory alotment
worker_mem = config['configurations']['alluxio-env']['alluxio.worker.memory']

# Find current stack and version to push agent files to
stack_name = default("/hostLevelParams/stack_name", None)
stack_version = config['hostLevelParams']['stack_version']

# hadoop params
namenode_address = None
if 'dfs.namenode.rpc-address' in config['configurations']['hdfs-site']:
  namenode_rpcaddress = config['configurations']['hdfs-site']['dfs.namenode.rpc-address']
  namenode_address = format("hdfs://{namenode_rpcaddress}")
else:
  namenode_address = config['configurations']['core-site']['fs.defaultFS']

host_name = config['hostname'];

alluxio_master = '#alluxio.master.hostname=' + host_name
alluxio_master_web_port = 'alluxio.master.web.port=' + config['configurations']['alluxio-env']['alluxio.master.web.port']

# HA
enabled_ha = 'alluxio.zookeeper.enabled=false'
zk_addr = '#alluxio.zookeeper.address=' + config['configurations']['alluxio-env']['alluxio.zookeeper.address']
journal_folder = 'alluxio.master.journal.folder=' + config['configurations']['alluxio-env']['alluxio.master.journal.folder']
worker_timeout = 'alluxio.worker.block.heartbeat.timeout.ms=120000'
if len(alluxio_masters) > 1:
  enabled_ha = 'alluxio.zookeeper.enabled=true'
  zk_addr = 'alluxio.zookeeper.address=' + config['configurations']['alluxio-env']['alluxio.zookeeper.address']
  journal_folder = 'alluxio.master.journal.folder=' + config['configurations']['alluxio-env']['alluxio.master.journal.folder']
  worker_timeout = 'alluxio.worker.block.heartbeat.timeout.ms=120000'
else:
  alluxio_master = 'alluxio.master.hostname=' + alluxio_masters[0]

# Set install dir
cmd = "/usr/bin/hdp-select versions"
usr_base = "/usr/hdp/"
base_dir = usr_base + commands.getoutput(cmd) + "/alluxio/"

# Alluxio archive on agent nodes
alluxio_package_dir = "/var/lib/ambari-agent/cache/stacks/" + stack_name + "/" + stack_version + "/services/ALLUXIO/package/"

# alluxio log dir
log_dir = config['configurations']['alluxio-env']['alluxio.log.dir']
journal_dir = config['configurations']['alluxio-env']['alluxio.master.journal.folder']

# alluxio hdd dirs
hdd_dirs = config['configurations']['alluxio-env']['alluxio.hdd.dirs']
hdd_quota = config['configurations']['alluxio-env']['alluxio.hdd.quota']

# alluxio pid dir
pid_dir = config['configurations']['alluxio-env']['alluxio.pid.dir']

# java_home = commands.getoutput('echo $JAVA_HOME')
