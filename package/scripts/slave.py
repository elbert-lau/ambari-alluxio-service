#import status properties defined in -env.xml file from status_params class

import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.base import Fail
from resource_management.core.exceptions import ComponentIsNotRunning
from subprocess import call
import cPickle as pickle

class Slave(Script):

  #Call setup.sh to install the service
  def install(self, env):
    import params
  
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    env.set_params(params)

    # Create the base_dir/alluxio dir
    cmd = '/bin/mkdir' + ' -p ' + params.base_dir
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    # Create the log_dir dir
    cmd = '/bin/mkdir' + ' -p ' + params.log_dir 
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    # Create the hdd_dirs dir
    cmd = '/bin/mkdir' + ' -p ' + params.hdd_dirs 
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    # Create the journal_dir dir
    cmd = '/bin/mkdir' + ' -p ' + params.journal_dir 
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    # Create the underfs_addr dir
    cmd = '/bin/mkdir' + ' -p ' + params.underfs_addr 
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    cmd = '/bin/tar' + ' -zxf ' + params.alluxio_package_dir + 'files/' +  params.alluxio_archive_file + ' --strip 1 -C ' + params.base_dir
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)
   
    cmd = '/bin/ln' + ' -s ' + params.base_dir  + ' ' + params.usr_base + 'current/'
    Execute('echo "Running ' + cmd + '"')
   
    try:
      Execute(cmd)
    except:
      pass

    self.configure(env)

  def configure(self, env):
    import params
    env.set_params(params)

    alluxio_config_dir = params.base_dir + 'conf/'
    alluxio_libexec_dir = params.base_dir + 'libexec/'

    # alluxio-env.sh
    File(format("{alluxio_config_dir}/alluxio-env.sh"),
          owner='root',
          group='root',
          content=Template('alluxio-env.sh.j2', conf_dir=alluxio_config_dir)
          )

    # alluxio-site.properties
    File(format("{alluxio_config_dir}/alluxio-site.properties"),
          owner='root',
          group='root',
          mode=0700,
          content=Template('alluxio-site.properties.j2', conf_dir=alluxio_config_dir)
          )

    # masters
    File(format("{alluxio_config_dir}/masters"),
          owner='root',
          group='root',
          mode=0700,
          content=Template('masters.j2', conf_dir=alluxio_config_dir)
          )

    # workers
    File(format("{alluxio_config_dir}/workers"),
          owner='root',
          group='root',
          mode=0700,
          content=Template('workers.j2', conf_dir=alluxio_config_dir)
          )

  #Call start.sh to start the service
  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)
    #Mount ramfs
    cmd = params.base_dir + 'bin/alluxio-start.sh ' + 'worker' + ' Mount'
    
    Execute('echo "Running cmd: ' + cmd + '"')
    Execute(cmd)

    # Create pid file - note check_process_status expects a SINGLE int in the file
    cmd = "mkdir -p " + params.pid_dir
    Execute(cmd)
    cmd = "echo `ps -A -o pid,command | grep -i \"[j]ava\" | grep AlluxioWorker | awk '{print $1}'`> " + params.pid_dir + "/AlluxioWorker.pid"
    Execute(cmd)

  #Called to stop the service using the pidfile
  def stop(self, env):
    import params
    env.set_params(params)
    self.configure(env)
    #execure the startup script
    cmd = params.base_dir + 'bin/alluxio-stop.sh ' + 'worker'

    Execute('echo "Running cmd: ' + cmd + '"')
    Execute(cmd)

  #Check pid file using Ambari check_process_status
  def status(self, env):
    check_process_status("/var/run/alluxio/AlluxioWorker.pid")

if __name__ == "__main__":
  Slave().execute()
