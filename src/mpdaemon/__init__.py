import subprocess

def get_output(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    proc.wait()
    out, _ = proc.communicate()
    return out

class MPDaemon(object):
    title = "Playlists"

    def is_running(self):
        return len(get_output(["mpc"]).split("\n")) == 4

    def is_playing(self):
        return get_output(["mpc"]).split("\n")[1].split()[0][1:-1] == "playing"

    def __get_playlists(self):
        return filter(lambda x: x[0].islower(), get_output(["mpc", "lsplaylists"]).strip().split("\n"))

    def __get_position(self):
        return get_output(["mpc"]).split("\n")[1].split()[1][1:]

    def __get_number(self):
        return int(self.__get_position().split("/")[0])

    def current(self):
        N = self.__get_number()-1
        artists = get_output(["mpc", "playlist", "-f", "%artist%"]).strip().split("\n")[N:]
        songs = get_output(["mpc", "playlist", "-f", "%title%"]).strip().split("\n")
        freqs = [(a, artists.count(a)) for a in set(artists)]
        freqs.sort(key=lambda x: -x[1])
        artist = freqs[0][0] # Most frequent artist

        return {"title": artist + " (" + self.__get_position() + ")",
                "songs": enumerate(songs),
                "position": self.__get_number(),
                }

    def library(self):
        playlists = self.__get_playlists()

        return sorted([{"id": playlist,
                        "title": playlist.title().replace("-", " "),
                        "image": None,
                        "description": "",
                        "rating": None,
                        "duration": None} for playlist in playlists], key=lambda x: x["title"])

    def pause(self): get_output(["mpc", "pause"])
    def play(self): get_output(["mpc", "play"])
    def skip(self, id): get_output(["mpc", "play", str(id)])

    def stop(self):
        get_output(["mpc", "clear"])
        subprocess.Popen(["vlc-server", "stop"], shell=True)
    
    def start(self, id):
        subprocess.Popen(["vlc-server", "mpd"], shell=True)
        get_output(["mpc", "clear"])
        if id == "*":
            import os
            os.system("mpc listall | mpc add")
        else:
            get_output(["mpc", "load", id])
        get_output(["mpc", "shuffle"])
        get_output(["mpc", "play"])

