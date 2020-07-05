import git
from urllib.request import Request
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime
import os.path
from os import path
import time
import argparse
import shutil
import sys
from colorama import init, Fore, Back, Style


def get_string(enterprise,directory):
    print(Fore.GREEN + "[MESSAGE] Looking for interesting words " + Back.RESET)
    now = datetime.now()
    timestamp = str(datetime.timestamp(now))
    email = str(str("@")+enterprise+".")
    #Edit this list to add new words
    lista = [";pass","storePassword","jdbc","DatabaseName",".password=","datasource.password","datasource.username","password=","Data Source=","Data Source =","password =","<password>","_password",email]
    for i in lista:
        print(Back.WHITE+"[SEARCH STRING]" + str(i)+Back.RESET)
        os.system("grep -rin '"+str(i)+"' --exclude=\*.css "+directory+"  | cut -b 1-280 >> GITHUB_"+str(enterprise)+"_"+str(timestamp)+"_LOG.txt")
    return (timestamp)

def git_CLONE(link,enterprise,directory,Repos):

    print(Fore.GREEN + "[MESSAGE] GIT-HUNTER will download: " + str(len(Repos)) + " Repositories. Check hard disk space." + Back.RESET)
    for i in Repos:
        now = datetime.now()
        timestamp = str(datetime.timestamp(now))
        os.mkdir(directory+timestamp, 0o755)
        print (Fore.WHITE+Back.BLUE+"[CLONE REPOSITORY] " + str(i) + Back.RESET)

        link = "https://github.com"+str(i)
        git.Git(directory+timestamp).clone(link)


def get_Repositories(pag_Repo,pag_Code,enterprise,directory,cookie,filename):
    print(Fore.GREEN + "[MESSAGE] Getting list of GITHUB Repositories" + Back.RESET)
    pagina_Repo = str(pag_Repo+1)
    pagina_Code = pag_Code

    # Checking if the cookie es valid
    if(pagina_Code==None):
        print(Fore.WHITE+Back.YELLOW + "[ALERT] Invalid Cookie value or there is not a Repositories - Check the value in your browser" + Back.RESET)
        pagina_Code = 0
    else:
        if(int(pagina_Code)!=0):
            pagina_Code = str(pag_Code + 1)

    enterprise = enterprise
    filename = filename
    directory = directory
    Repos =[]


    for y in range(1,int(pagina_Repo)):
        url = "https://github.com/search?p=" + str(y) + "&q="+str(enterprise)+"&type=Repositories"
        req = Request(url)
        req.add_header('Cookie', 'user_session='+str(cookie))

        print(Fore.YELLOW + "[URL] " + url + Back.RESET)
        with urllib.request.urlopen(req) as response:
            resp = response.read()
            soup = BeautifulSoup(resp, "html.parser")
            for link in soup.find_all('a', {'class': 'v-align-middle'}):
                link = link['href']
                Repos.append(link)
        #Add to wait 3 or 10 seconds in each request (Solve the problem about HTTP ERROR 429 TOO MANY REQUEST
        if(cookie==None):
            #if the cookie is NONE or invalid (very slow)
            time.sleep(10)
        else:
            #To better results use a valid cookie (fast)
            time.sleep(3)



    if (int(pagina_Code)>0) and (pagina_Code != None):
        for x in range(1, int(pagina_Code)):
            url = "https://github.com/search?p=" + str(x) + "&q=filename%3A" + str(filename) + "+" + str(enterprise) + "&type=Code"
            req = Request(url)
            req.add_header('Cookie', 'user_session=' + str(cookie))

            print(Fore.YELLOW + "[URL] " + url + Back.RESET)
            with urllib.request.urlopen(req) as response:
                resp = response.read()
                soup = BeautifulSoup(resp, "html.parser")
                for link in soup.find_all('a', {'class': 'link-gray'}):
                    link = link['href']
                    Repos.append(link)
            # Add to wait 3 seconds in each request
            time.sleep(3)

    Repos = list(set(Repos))
    git_CLONE(link,enterprise,directory,Repos)
    timestamp=get_string(enterprise,directory)
    return(timestamp)



def get_PAG_Code(enterprise,filename,cookie):
    #Getting the page number of the CODE SECCTION
    enterprise = enterprise
    filename = filename
    cookie = cookie
    url = "https://github.com/search?q=filename%3A" + str(filename) + "+"+str(enterprise)+"&type=Code"
    req = Request(url)
    req.add_header('Cookie', 'user_session='+str(cookie))

    with urllib.request.urlopen(req) as response:
        resp = response.read()
        soup = BeautifulSoup(resp, "html.parser")
        cont = 0

        for page in soup.find_all('span', {'class': 'ml-1 mt-1 js-codesearch-count Counter Counter--gray'}):
            cont = cont +1
            if (cont==2):

                if (str(page.string) == "1K"):
                    print(
                        Fore.WHITE + Back.YELLOW + "[ALERT] There are 1K or more repositories. GIT-HUNTER will download only 100 repositores." + Back.RESET)
                    return (10)

                if (int(page.string) <= 10):
                    return (1)
                else:
                    total = int(page.string) / 10
                    pag = int(page.string) // 10
                    rest = total % 10
                    if (rest > 0):
                        pag = pag + 1
                        return (pag)


def get_PAG_Repositories(enterprise,filename, cookie):
    #print("Getting the page number of the REPOSITORY SECTION")
    enterprise = enterprise
    url = 'https://github.com/search?p=1&q='+str(enterprise)+'&type=Repositories'

    with urllib.request.urlopen(url) as response:
        resp = response.read()
        soup = BeautifulSoup(resp, "html.parser")

        for page in soup.find_all('span', {'class': 'ml-1 mt-1 js-codesearch-count Counter Counter--gray'}):

            if (str(page.string) == "1K"):
                print(Fore.WHITE + Back.YELLOW + "[ALERT] There are 1K or more repositories. GIT-HUNTER will download only 100 repositores." + Back.RESET)
                return (10)

            if (int(page.string) <= 10):
                return (1)
            else:
                total = int(page.string) / 10
                pag = int(page.string) // 10
                rest = total % 10
                if (rest > 0):
                    pag = pag + 1
                    return (pag)



def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A tool to get information of GIT Repository',
        epilog='Author: Omar Palomino (A.K.A - EL PALOMO) | elpalomo.pe')
    parser.add_argument('enterprise', type=str, help='Name of enterprise to get repositories')
    parser.add_argument('-f', '--filename', type=str, help='Github Dork FILENAME', default=None)
    parser.add_argument('-c', '--cookie', type=str, help='User_Session cookie to use --filename option', default=None)
    parser.add_argument('-d', '--directory', type=str, help='Folder to download repositories', default=".")
    return parser.parse_args()


def main():
    args = parse_arguments()
    enterprise = args.enterprise
    directory= args.directory + "/" + enterprise + "/"
    filename = args.filename
    cookie = args.cookie

    # Check if exist the directory to download the repositories
    if(path.exists(directory)==True):
        n= input(Fore.WHITE+Back.YELLOW + "[ALERT] The directory is not empty. Do you want delete the '"+str(directory)+"' folder? (N/y)" + Back.RESET)
        if(str(n)=="y" or str(n)=="Y"):
            shutil.rmtree(directory)
            os.mkdir(directory, 0o755)
        else:
            print(Fore.GREEN + "[MESSAGE] You need select another directory to clone the Repositories" + Back.RESET)
            sys.exit()
    else:
        os.mkdir(directory, 0o755)

    pag_Repo = get_PAG_Repositories(enterprise,filename,cookie)
    #Valide the options to run the script
    if(filename!=None):
        if(cookie!=None):
            pag_Code = get_PAG_Code(enterprise, filename, cookie)
        else:
            print(Fore.WHITE+Back.YELLOW + "[ALERT] - You need add a COOKIE VALUE if you use the -f or --filename option" + Back.RESET)
            pag_Code = None
    else:
        if(cookie!=None):
            print(Fore.WHITE+Back.YELLOW + "[ALERT] - You need add -f or --filename option if you use the COOKIE option" + Back.RESET)
        pag_Code = None

    timestamp= get_Repositories(pag_Repo,pag_Code,enterprise,directory,cookie,filename)
    print("[MESSAGE] You can see the result in GITHUB_"+str(enterprise)+"_"+str(timestamp)+"_LOG.txt. Happy Hacking! wq!")

if __name__ == '__main__':
    main()