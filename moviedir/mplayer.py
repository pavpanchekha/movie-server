import subprocess
import os

import cPickle as pickle

MPLAYER="/usr/bin/mplayer"
FIFO="mplayer.fifo"
STATE="mplayer.pickle"

class MPlayer(object):
    def __init__(self, dir):
        self.dir = dir
        if os.path.exists(STATE):
            self.state = pickle.load(open(STATE, "rb"))
        else:
            self.state = {"playing": False, "movie": None}
            self.sync_state()

    def sync_state(self):
        pickle.dump(self.state, open(STATE, "wb"))

    def make_fifo(self):
        if os.path.exists(FIFO):
            self.rm_fifo()
        os.mkfifo(FIFO)

    def rm_fifo(self):
        os.unlink(FIFO)
    
    def start(self, f):
        if self.state["movie"] is not None:
            self.stop()
        self.state["movie"] = f
        self.state["playing"] = True
        self.make_fifo()
        subprocess.Popen([MPLAYER, "-fs", "-idle", "-slave", "-really-quiet", "-input", "file="+os.path.abspath(FIFO), os.path.abspath(os.path.join(self.dir, f))], stderr=open("/dev/null"), stdout=open("/dev/null"))
        self.sync_state()

    def send_command(self, cmd):
        with open(FIFO, "w") as f:
            f.write(cmd + "\n")

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
        self.rm_fifo()
