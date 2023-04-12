
from steamship import Steamship, MimeTypes, File
from pathlib import Path


class ContentCast:

    def __init__(self, instance_handle, package = "contentcast", index_name = "contentcastindex"):
        
        config={"index_name": index_name}
        self.client = Steamship.use(
            package,
            instance_handle=instance_handle,
            config = config
        )

    def addTranscript(self, transcript):
        resp = self.client.invoke(
             "add_transcript",
             name="CS Podcast",   
             transcript=transcript
         )
        return resp
    
    #I'd love for this method to return a list of relevant podcasts + an answer of chatGPT per podcast to the question
    def askQuestion(self, topic):
        resp =self.client.invoke(
            "answer",
            question="What unique tips & tricks are being shared about "+topic+"? Make sure they aren't self-evident. They have to be refreshing and non-obvious. Provide me with a specific exerpt of the text and pretend it's a quote. Then provide some more context yourself. Do this for every interesting insight, not just once."
        )
        return resp


    def getDocuments(self):
        resp = self.client.invoke(
            "documents",
            verb="GET"
        )
        return resp