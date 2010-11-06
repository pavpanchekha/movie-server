import config
import base64
import os

class Movie(object):
    def __init__(self, f):
        self.f = f
        self.prefix = ".".join(self.f.split(".")[:-1])

        try:
            with open(os.path.join(config.MOVIE_DIR, "meta", self.prefix+".txt")) as f:
                lines = f.readlines()
                title, chunk = lines[0].rsplit("(", 1)
                self.title = title.strip()
                self.year = int(chunk.split(")")[0])
                self.rating = int(lines[1].count("*") / float(lines[1].count(".") + lines[1].count("*")) * 5)
                self.summary = "".join(lines[3:]).replace("\n", " ")
        except IOError:
            self.title = self.prefix
            self.year = 2010
            self.rating = 0
            self.summary = ""

    @property
    def thumbnail(self):
        try:
            img = open(os.path.join(config.MOVIE_DIR, "covers", self.prefix + ".jpg"), "rb").read()
        except IOError:
            img = open(os.path.join(config.MOVIE_DIR, "covers", "missing.jpg"), "rb").read()
        return base64.b64encode(img)

    @property
    def duration(self):
        import subprocess
        proc = subprocess.Popen(["ffprobe", os.path.join(config.MOVIE_DIR, self.f)], stderr=subprocess.PIPE)
        proc.wait()
        _, data = proc.communicate()
        duration_line = [line for line in data.split("\n") if "Duration" in line][0]
        hrs,min,sec = map(float, duration_line.strip().split()[1][:-1].split(":"))
        return sec/60 + min + hrs*60, "%02d:%02d" % (hrs, min)


