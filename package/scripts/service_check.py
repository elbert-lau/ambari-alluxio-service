#!/usr/bin/env python
from resource_management import *
import subprocess
 
class AlluxioServiceCheck(Script):
  # Service check for Alluxio service
  def service_check(self, env):
    import params
 
    env.set_params(params)
    target_host = format("{alluxio_master}")
    print ('Service check host is: ' + target_host)
    full_command = [ "ssh", target_host, params.base_dir + "/bin/alluxio", "runTests"]
    proc = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    response = stdout
 
    # response is
    # Passed the test
    # or
    # Failed the test!
 
    if 'Failed' in response:
      raise ComponentIsNotRunning()
 
if __name__ == "__main__":
  AlluxioServiceCheck().execute()
