import subprocess
cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
for line in proc.stdout:
    if not line.decode()[0].isspace():
        print(line.decode().rstrip())
        