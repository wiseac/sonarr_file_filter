from arrapi import SonarrAPI
from typing import List, Union
import json,os

animelist= [2]

class SonarrFilter:
    def __init__(self):
        secrets = self.get_secrets()

        self.api_key = secrets['api-key']
        self.localhost = secrets['localhost']
        self.tag = secrets['genre']

        self.sonarr = SonarrAPI(self.localhost, self.api_key)
        self.series = self.sonarr.all_series()


    def get_secrets(self):
        path=os.path.dirname(os.path.abspath(__file__)) 
        
        with open(f'{path}/secrets.json') as f:
            d=f.read()

        return json.loads(d)
    
    def update_series(self):
        self.series = self.sonarr.all_series()

    
    def remove_tag(self):
        self.series = self.sonarr.all_series()
        for show in self.series:
            if show.genres.count(str(self.tag)) == 0 and 2 in show.tagsIds and show.seriesType != str(self.tag).lower():
                self.sonarr.edit_series(series_id=show.id,tags=animelist, apply_tags="remove")
                


    def add_tag(self):
        self.series = self.sonarr.all_series()
        for show in self.series:
            if show.genres.count(str(self.tag)) > 0 and 2 not in show.tagsIds or show.seriesType == str(self.tag).lower():
                self.sonarr.edit_series(series_id=show.id,tags=animelist, apply_tags="add")
                
 

    def moveout_show(self):
        self.series = self.sonarr.all_series()
        for show in self.series:
            if show.tagsIds == [] and show.rootFolderPath == "/"+str(self.tag).lower():
                self.sonarr.edit_series(series_id=show.id,path="/tv/"+str(show.title), move_files=True)
        


    def movein_show(self):
        self.series = self.sonarr.all_series()
        for show in self.series:
            if 2 in show.tagsIds and show.rootFolderPath != "/"+str(self.tag).lower():
                self.sonarr.edit_series(series_id=show.id,path="/"+str(self.tag).lower()+"/"+str(show.title), move_files=True)
   

    def run_all(self):
        self.remove_tag()
        self.add_tag()
        self.moveout_show()
        self.movein_show()
    


sf = SonarrFilter()
sf.run_all()


