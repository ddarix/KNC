# KNC

## KNX NetCat Handler

This simple script handle standard nc reverse shell (from linux and windows) and elevate it to a full TTY shell.
Thx to socat and ConPtyShell [@splintercode](https://github.com/antonioCoco)

## Requisities
- pwntools

## Usage

You have to put knc.py, socat, conpty in the same directory and run conpty with pyhton3.

Example:

```
python3 knc.py -l 192.168.1.45 80
```

## Installation
Clone the repo and be sure pwntools is installed
```
pip install pwntools
```

You can also make a symlink for your convenience.

## How it works
knc starts a tcp listener on the port specified in the standard input and waits for an incoming connection.

When a new connection arrives, it copies socat or ConptyShell, in linux or windows, respectively, through a simple echo of the base64-encoded binary, decodes it and executes it by sending back a shell with socat or with ConptyShell.

> NOTE: In linux once you receive the shell copy the tool output string into standard input and press enter to set the terminal with the correct parameters.

**TODO: Automate this last step as well.**



In linux socat allows a full TTY with history, autocomplete commands, intercepts CTRL+C so as not to kill the shell by mistake, allows using arrows to go back in case of errors or to recall previous commands. It also allows editing files with vim, nano and all other editors that require an interactive shell.

In windows ConPtyShell allows you to have a fully interactive Powershell reverse shell, with autocompletion of commands and their parameters, also allows the use of arrows.

## Final note for paranoid users

If you don't trust the 2 base64 encoded files, you can decode them into a binary file and reverse engineer them to verify the contents.

Alternatively, you can generate them yourself:

**socat linux:**
Using the statically compiled version of socat 64 bit for linux run a trivial:
```
cat <socat> |base64 -wo
```

**ConPtyShell**
From the official [@splintercode](https://github.com/antonioCoco/ConPtyShell) repo compile the version in .cs and then encode it in base64 using certutil from a windows terminal:
```
certutil -encode <path\ConPtyShell.exe> <output_path\conpty>.
```
