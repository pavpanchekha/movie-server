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
    
    def current(self):
        """Return information about the current movie"""

        curr = Movie(self.dir, self.control.state["movie"])

        return {
            "title": "%s (%d)" % (curr.title, curr.year),
            "image": curr.thumbnail,
            "description": curr.summary,
            "rating": curr.rating,
            "duration": curr.duration[1],
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
                       "duration": mov.duration[1]} for mov in library], key=lambda x: x["title"])

    def pause(self): self.control.pause()
    def play(self): self.control.play()
    def stop(self): self.control.stop()
    def start(self, id): self.control.start(id)

def VLCDir(dir="/var/movies", tmpdir="/tmp"):
    from vlc import VLC
    return MovieDir(VLC, dir, tmpdir)
