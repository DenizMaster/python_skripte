from fabric import task

HOSTS=["10.42.0.1"]
@task(hosts=HOSTS)
def hello(c):
    c.run('ls')

@task(hosts=HOSTS)
def test_board(c):
    c.run('BOARD=nucleo-l073rz make -C ~/RIOT/tests/driver_sx1280 term')

@task(hosts=HOSTS)
def test_empfanger(c):
    c.put("/home/lora/Dokumente/lora_empfanger.py", "/home/lora/pythonscript/python_skripte/lora_empfanger.py")
    c.run('cd /home/lora/pythonscript/python_skripte/ && python -u lora_empfanger.py 1 2 3')

@task(hosts=HOSTS)
def ls(c):
    c.run('ls -l')

@task(hosts=HOSTS)
def zeigen(c):
    c.run('tail -f /home/lora/Dokumente/debugmitschrift.txt')

@task(hosts=HOSTS)
def erstelltest(c):
    c.run('touch /home/lora/Documents/CSV_datei/endesingnal.txt')

@task(hosts=HOSTS)
def loschtest(c):
    c.run('rm -f /home/lora/Documents/CSV_datei/endesingnal.txt')

@task(hosts=HOSTS)
def logg(c):
    c.run('cat /tmp/output.txt')

@task(hosts=HOSTS)
def debug(c):
    c.run('cat /home/lora/Documents/CSV_datei/testdaten.dat')


    
   