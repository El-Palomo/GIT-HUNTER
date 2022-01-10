# GIT-HUNTER
Python tool to detect critical information (passwords, usernames, strings connectios, etc) in public repositories. GITHUB Hacking.

## Installation
```
- git clone https://github.com/El-Palomo/GIT-HUNTER
- cd GIT-HUNTER
- python3 git_hunter.py -h
``` 

## Usage
GIT-HUNTER script only works in Python3.
```
usage: git_hunter.py [-h] [-f FILENAME] [-c COOKIE] [-d DIRECTORY] enterprise

A tool to get information of GIT Repository

positional arguments:
  enterprise            Name of enterprise to get repositories

optional arguments:
  -h, --help                            show this help message and exit
  -f FILENAME, --filename FILENAME      Github Dork FILENAME
  -c COOKIE, --cookie COOKIE            User_Session cookie to use --filename option
  -d DIRECTORY, --directory DIRECTORY   Folder to download repositories

Author: Omar Palomino (A.K.A - EL PALOMO) | elpalomo.pe
```
- Method 1: 
Only search in the REPOSITORY section of Github.
  1. Select an enterprise/organization in Github.
  2. You can use GIT-HUNTER with the following command:
    ```
    root@kali:~/GIT-HUNTER# python3 git_hunter.py -d /opt enterprise
    ```
  3. You can see the result in GITHUB_enterprise_log.txt file.

- Method 2:
Use the --filename and --cookie options to get more repositories and more information.
  1. Select an enterprise/organization in Github.
  2. Login in GITHUB and get the "user_session" cookie value to use with the --cookie option. There are many ways to get the cookie.
  3. Select a file type to  use wiht the --filename option. PROPERTIES or CONFIG file for example.
  4. Run GIT-HUNTER with the following command:
    ```
    root@kali:~/GIT-HUNTER# python3 git_hunter.py -d /opt -f properties -c [USER_SESSION_COOKIE] enterprise
    ```
  5. You can see the result in GITHUB_enterprise_log.txt file.

## Customize and next steps
1. If you need search more strings, edit the line 18 and add the word that you need.
2. For the next version of GIT-HUNTER, I'll add more dorks posibilities.
3. For best results, manually search on github.

## Requirements
1. The script was tested in Kali Linux 2020.2 and not need install any library.
2. If you use another Linux distro or other Kali Linux version. You need install the following libraries for python3:
* URLLIB
* GIT
* COLORAMA
* BEATIFULSOUP
* SHUTIL

# Demo
https://youtu.be/17npWCv-l1g

[![IMAGE ALT TEXT HERE](https://i3.ytimg.com/vi/17npWCv-l1g/maxresdefault.jpg)](https://youtu.be/17npWCv-l1g)


<img src="https://github.com/El-Palomo/GIT-HUNTER/blob/master/example/1_example.png" width="30%"></img> <img src="https://github.com/El-Palomo/GIT-HUNTER/blob/master/example/2_example.png" width="30%"></img> <img src="https://github.com/El-Palomo/GIT-HUNTER/blob/master/example/3_example.png" width="30%"></img> <img src="https://github.com/El-Palomo/GIT-HUNTER/blob/master/example/4_example.png" width="30%"></img>
