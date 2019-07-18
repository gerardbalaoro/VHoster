import subprocess

class Console:
    
    def run(self, command, *args):
        subprocess.call([command, *args])