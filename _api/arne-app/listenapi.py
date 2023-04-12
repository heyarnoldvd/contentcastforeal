from steamship import Steamship, MimeTypes, File
from bs4 import BeautifulSoup
from steamship.base import TaskState
from listennotes import podcast_api
import time

API_KEY='3772755958c549278891282bdaf5e9f1'
HAS_LISTEN_NOTES_PRO = False
MAX_PODCASTS_LOAD = 30


class Podcast:

    def __init__(self, id, audio, image, title_original, description_original):
        self.id = id
        self.audio = audio
        self.image = image
        self.title = BeautifulSoup(title_original, features="lxml").get_text()
        self.description = BeautifulSoup(description_original, features="lxml").get_text()
        
        self.hasTranscript = False
        self.transcript = ""

    #Can take a long while to execute
    def getTranscript(self, useSteamship=True):
        if not self.hasTranscript:
           transcript = ListenAPI().getTranscript(self.id)
           if transcript == "":
                return ""
           else:
                #get transcript from steamship
                if useSteamship:
                    transcript = self.__getTranscriptFromSteamship()
                    self.hasTranscript = True 
                    return transcript
                return ""
        return ""
    
    def __getTranscriptFromSteamship(self):
        
        pkgAudio = Steamship.use(
            "audio-analytics",
            instance_handle="audio-analytics-9da"
        )
        transcribe_task =pkgAudio.invoke("analyze_url", url=self.audio)
        task_id = transcribe_task["task_id"]
        status = transcribe_task["status"]

        n_retries = 0
        while n_retries <= 100 and transcribe_task["status"] != TaskState.succeeded:
            transcribe_task = pkgAudio.invoke("status", task_id=task_id)
            time.sleep(2)

        file = transcribe_task["file"]
        file = File.parse_obj(file)

        block = file.blocks[0]
        transcription = block.text
        return transcription
    
    def __getGuestNames():
        return ""
    

class ListenAPI:

    def __init__(self):
        self.client = podcast_api.Client(api_key=API_KEY)

    def getTranscript(self, id):
        if not HAS_LISTEN_NOTES_PRO:
            return ""
        episode = self.client.fetch_episode_by_id(id=id,show_transcript=1).json()
        return episode["transcript"] 

    def search(self,query):
        #sort_by_date=1 to stort by date
        return self.searchIteration(query)

    def searchIteration(self,query,offset=0):
        if offset*10 > MAX_PODCASTS_LOAD:
            return []
        else:
            results = self.client.search(q=query,offset=offset)
            return [Podcast(r["id"], r["audio"], r["image"], r["title_original"], r["description_original"]) for r in results.json()["results"]] + self.searchIteration(self,offset+10)
            