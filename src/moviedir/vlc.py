import subprocess
import os
import socket
import cPickle as pickle

VLCBINARY = "/usr/bin/vlc"

class VLC(object):
    def __init__(self, dir, tmpdir):
        self.STATE = os.path.join(tmpdir, "vlc.pickle")
        
        self.dir = dir
        if os.path.exists(self.STATE):
            self.state = pickle.load(open(self.STATE, "rb"))
        else:
            self.state = {"playing": False, "movie": None, "socket": None}
            self.sync_state()

    def sync_state(self):
        pickle.dump(self.state, open(self.STATE, "wb"))

    def start(self, f):
        if self.state["movie"] is not None:
            self.stop()
        self.state["movie"] = f
        self.state["playing"] = True
        vlc = subprocess.Popen(["bash", "-c", "vlc-server file % s" % os.path.abspath(os.path.join(self.dir, f))], shell=True, stdout=subprocess.PIPE)
        addr, _ = vlc.communicate()
        self.state["socket"] = tuple(addr.rsplit(":", 1))
        self.sync_state()

    def send_command(self, cmd):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(*self.state["socket"])
        except IOError:
            self.state["movie"] = None
            self.state["playing"] = False
            self.sync_state()
        else:
            s.send(cmd + "\n")
        
        s.close()

    def pause(self):
        assert self.state["playing"], "Attempting to pause paused movie"
        self.send_command("pause")
        self.state["playing"] = False
        self.sync_state()

    def play(self):
        assert not self.state["playing"], "Attempting to unpause unpaused movie"
        self.send_command("play")
        self.state["playing"] = True
        self.sync_state()
    
    def stop(self):
        self.state["movie"] = None
        self.state["playing"] = False
        self.state["socket"] = None
        self.sync_state()
        subprocess.Popen(["bash", "-c", "vlc-server stop"], shell=True)
