from mplayer import MPlayer
from moviedata import Movie
import os

class MovieDir(object):
    title = "Movies" # Type of object allowed

    def __init__(self, dir="/var/movies", tmpdir="/tmp"):
        self.dir = dir
        self.mplayer = MPlayer(self.dir, tmpdir=tmpdir)

    def is_running(self):
        return self.mplayer.state["movie"] is not None

    def is_playing(self):
        return self.mplayer.state["playing"]
    
    def current(self):
        """Return information about the current movie"""

        curr = Movie(self.dir, self.mplayer.state["movie"])

        return {
            "title": "%s (%d)" % (curr.title, curr.year),
            "image": curr.thumbnail,
            "description": curr.summary,
            "rating": curr.rating,
            "meta": {"duration": curr.duration[1]},
            }

    def library(self):
        """Return list of available movies"""

        library = [os.path.join(self.dir, file) for file in os.listdir(self.dir)]
        library = [Movie(self.dir, os.path.split(x)[-1]) for x in library if os.path.isfile(x)]
        return sorted([{"id": mov.f,
                       "title": mov.title,
                       "description": mov.summary,
                       "rating": mov.rating,
                       "image": mov.thumbnail,
                       "meta": {"duration": mov.duration[1]}} for mov in library], key=lambda x: x["title"])

    def pause(self): self.mplayer.pause()
    def play(self): self.mplayer.play()
    def stop(self): self.mplayer.stop()
    def start(self, id): self.mplayer.start(id)
