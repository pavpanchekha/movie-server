import subprocess
import os

import cPickle as pickle

MPLAYER="/usr/bin/mplayer"

class MPlayer(object):
    def __init__(self, dir, tmpdir):
        self.FIFO = os.path.join(tmpdir, "mplayer.fifo")
        self.STATE = os.path.join(tmpdir, "mplayer.pickle")
        
        self.dir = dir
        if os.path.exists(self.STATE):
            self.state = pickle.load(open(self.STATE, "rb"))
        else:
            self.state = {"playing": False, "movie": None}
            self.sync_state()

    def sync_state(self):
        pickle.dump(self.state, open(self.STATE, "wb"))

    def make_fifo(self):
        if os.path.exists(self.FIFO):
            self.rm_fifo()
        os.mkfifo(self.FIFO)

    def rm_fifo(self):
        os.unlink(self.FIFO)
    
    def start(self, f):
        if self.state["movie"] is not None:
            self.stop()
        self.state["movie"] = f
        self.state["playing"] = True
        self.make_fifo()
        subprocess.Popen([MPLAYER, "-fs", "-zoom", "-display", ":0.0", "-idle", "-slave", "-input", "file="+os.path.abspath(self.FIFO), os.path.abspath(os.path.join(self.dir, f))], stderr=open("/dev/null"))
        self.sync_state()

    def send_command(self, cmd):
<<<<<<< HEAD:moviedir/mplayer.py
        with open(self.FIFO, "w") as f:
            f.write(cmd + "\n")
=======
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.connect(self.SOCKET)
        except socket.error:
            self.state["movie"] = None
            self.state["playing"] = False
            self.sync_state()
            return
        s.send(cmd + "\n")
        s.close()
>>>>>>> VLC not running detected:moviedir/vlc.py

    def pause(self):
        assert self.state["playing"], "Attempting to pause paused movie"
        self.state["playing"] = False
        self.send_command("pause")
        self.sync_state()

    def play(self):
        assert not self.state["playing"], "Attempting to unpause unpaused movie"
        self.state["playing"] = True
        self.send_command("pause")
        self.sync_state()
    
    def stop(self):
        self.state["movie"] = None
        self.state["playing"] = False
        self.sync_state()
        self.send_command("quit")
        self.rm_fifo()
