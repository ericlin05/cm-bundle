
#import urllib2
#mp3file = urllib2.urlopen("http://host-10-17-100-146.coe.cloudera.com:7180/cmf/command/782/download")
#with open('bundle.zip','wb') as output:
#  output.write(mp3file.read())

import pycurl
from cm_api.api_client import ApiResource
from cm_api.endpoints.cms import ClouderaManager
from datetime import date

cluster_name = "cluster"
host_url = "host-10-17-100-146.coe.cloudera.com"

api = ApiResource(
    host_url,
    username="admin",
    password="admin",
)

end_time = date(2017, 12, 18)
cm = ClouderaManager(api)
cmd = cm.collect_diagnostic_data_45(end_time, 1073741824, cluster_name)

if not cmd.wait().success:
    raise Exception("Failed to run cluster diagnositc bundle collection")

result_data_url = "http://" + host_url + ":7180/cmf/command/" + str(cmd.id) + "/download" 
print result_data_url
print getattr(cmd, "id")
print getattr(cmd, "name")
print cmd.to_json_dict(True)

print cmd.id
print cmd.name
print cmd.resultDataUrl

# As long as the file is opened in binary mode, both Python 2 and Python 3
# can write response body to it without decoding.
with open('bundle.zip', 'wb') as f:
    c = pycurl.Curl()
    c.setopt(c.URL,  result_data_url)
    c.setopt(c.USERPWD, 'admin:admin')
    c.setopt(c.WRITEDATA, f)
    c.perform()
    c.close()

