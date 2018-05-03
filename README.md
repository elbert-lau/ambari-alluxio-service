## Alluxio Service for Ambari 2.6.1.5 (HDP 2.6.4.0)

Alluxio v 1.6.1 - Deploys on HDP 2.6.4.0


Install, start/stop, status, service check functional


**1. Clone the service into the dir for the Stack you are running in Ambari**

**- Adding Alluxio to a HDP 2.6 Cluster**

```
# Clone the service deployer
git clone https://github.com/elbert-lau/ambari-alluxio-service /var/lib/ambari-server/resources/stacks/HDP/2.6/services/ALLUXIO

#git has a 100mb file limit, download alluxio source to your stack dir
wget http://alluxio.org/downloads/files/1.6.1/alluxio-1.6.1-bin.tar.gz -P /var/lib/ambari-server/resources/stacks/HDP/2.6/services/ALLUXIO/package/files 

ambari-server restart

```


**2. Add service via Ambari ui**



**3. Assign a Alluxio Master And Worker nodes.**

By default the master will also run a worker 


Once Service is started, you may access Alluxio Master Web UI on ***alluxio.master.hostname*:19999**

**Future Work:**
Use non-root user 
defaultFS url
Metrics
Fix status check on start
Clean up & Expand alluxio-env

**Reference**
https://github.com/chuyqa/alluxio-ambari-service
