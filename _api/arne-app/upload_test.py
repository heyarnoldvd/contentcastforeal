
from steamship import Steamship, MimeTypes, File
from pathlib import Path

from listenapi import ListenAPI, Podcast
from contentcast import ContentCast

from steamship.base import TaskState

instance_handle = "cc2"
txt = Path('_api/upload/cs-podcast.txt').read_text()
podcastURL = "https://www.listennotes.com/e/p/62ac994218a54960b835fa1d457f5d18/"


cc = ContentCast(instance_handle)
result = cc.askQuestion("customer retention")
print(result["answer"])

### GET PODCAST FROM LISTENAPI ###
#api = ListenAPI()
#results = api.search('customer success') 

#print(results)