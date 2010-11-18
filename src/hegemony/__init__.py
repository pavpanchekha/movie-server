import subprocess

class Hegemony(object):
    def __init__(self, hosts):
        self.hosts = hosts
    
    def start(self, host):
        assert host in self.hosts, "Unknown host"
        subprocess.Popen(["bash", "-c", "vlc-client start %s" % host]).wait()
    
    def stop(self, host):
        assert host in self.hosts, "Unknown host"
        subprocess.Popen(["bash", "-c", "vlc-client stop %s" % host]).wait()

    def restart(self, host):
        assert host in self.hosts, "Unknown host"
        subprocess.Popen(["bash", "-c", "vlc-client restart %s" % host]).wait()

    def status(self, host):
        assert host in self.hosts, "Unknown host"
        proc = subprocess.Popen(["bash", "-c", "vlc-client status %s" % host], stdout=subprocess.PIPE)
        out, _ = proc.communicate()
        return out.count("\n") == 1

    def status_all(self):
        return dict((host, self.status(host)) for host in self.hosts)

