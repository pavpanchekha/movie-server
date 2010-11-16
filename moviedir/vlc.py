import subprocess
import os
import socket
import cPickle as pickle

VLCBINARY = "/usr/bin/vlc"

class VLC(object):
    def __init__(self, dir, tmpdir):
        self.SOCKET = os.path.join(tmpdir, "mplayer.sock")
        self.STATE = os.path.join(tmpdir, "mplayer.pickle")
        
        self.dir = dir
        if os.path.exists(self.STATE):
            self.state = pickle.load(open(self.STATE, "rb"))
        else:
            self.state = {"playing": False, "movie": None}
            self.sync_state()

    def sync_state(self):
        pickle.dump(self.state, open(self.STATE, "wb"))

    def start(self, f):
        if self.state["movie"] is not None:
            self.stop()
        self.state["movie"] = f
        self.state["playing"] = True
        subprocess.Popen([VLCBINARY, "-f", "--x11-display", ":0.0", "-I", "rc", "--rc-unix="+os.path.abspath(self.SOCKET), "--rc-fake-tty", os.path.abspath(os.path.join(self.dir, f))], stderr=open("/dev/null"))
        self.sync_state()

    def send_command(self, cmd):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.SOCKET)
        s.send(cmd + "\n")
        s.close()

    def pause(self):
        assert self.state["playing"], "Attempting to pause paused movie"
        self.send_command("pause")
        self.state["playing"] = False
        self.sync_state()

    def play(self):
        assert not self.state["playing"], "Attempting to unpause unpaused movie"
        self.send_command("pause")
        self.state["playing"] = True
        self.sync_state()
    
    def stop(self):
        self.state["movie"] = None
        self.state["playing"] = False
        self.sync_state()
        self.send_command("quit")
