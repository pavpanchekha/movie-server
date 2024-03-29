from moviedata import Movie
import os

class MovieDir(object):
    title = "Movies" # Type of object allowed

    def __init__(self, controller, dir="/var/movies", tmpdir="/tmp"):
        self.dir = dir
        self.control = controller(self.dir, tmpdir=tmpdir)

    def is_running(self):
        return self.control.state["movie"] is not None

    def is_playing(self):
        return self.control.state["playing"]

    def info(self, id):
        """Return information about a given id"""
        
        curr = Movie(self.dir, id)

        return {
            "title": "%s (%s)" % (curr.title, curr.year),
            "image": curr.thumbnail,
            "description": curr.summary,
            "rating": curr.rating,
            "duration": curr.duration[1],
            }
    
    def current(self):
        """Return the id of the current movie"""

        return self.control.state["movie"]
    
    def library(self):
        """Return list of available movies"""

        library = [os.path.join(self.dir, file) for file in os.listdir(self.dir)]
        library = [Movie(self.dir, os.path.split(x)[-1]) for x in library if os.path.isfile(x)]
        return sorted([{"id": mov.f,
                       "title": mov.title,
                       "description": mov.summary,
                       "rating": mov.rating,
                       "image": mov.thumbnail,
                       "duration": mov.duration[1]} for mov in library], key=lambda x: x["title"])

    def pause(self): self.control.pause()
    def play(self): self.control.play()
    def stop(self): self.control.stop()
    def start(self, id): self.control.start(id)

def VLCDir(dir="/var/movies", tmpdir="/tmp"):
    from vlc import VLC
    return MovieDir(VLC, dir, tmpdir)
