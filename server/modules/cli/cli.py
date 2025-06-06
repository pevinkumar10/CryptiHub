try:
    import sys
    import argparse
    import requests
    from colorama import Fore,Style 

    red=Fore.RED
    blue=Fore.BLUE
    white=Fore.WHITE
    magenta=Fore.MAGENTA
    bright=Style.BRIGHT
    green=Fore.GREEN
    red=Fore.RED
    bold=Style.BRIGHT
    yellow=Fore.YELLOW
    cyan=Fore.CYAN
    mixed=Fore.BLUE+Fore.GREEN+Fore.RED
    reset=Style.RESET_ALL
    
except ImportError as Ie:
    print(f"Error [Core]: {Ie}")

class CommandLine():
    def args(self):
        # Function to parse arguments.
        parser=argparse.ArgumentParser(add_help=False,usage=argparse.SUPPRESS,exit_on_error=False)
        try:
            parser.add_argument("-nb","--no-banner",action="store_true")
            parser.add_argument("-v","--version",action="store_true")
            parser.add_argument("-h","--help",action="store_true")
            
            args=parser.parse_args()
            return args
        
        except argparse.ArgumentError:
            print(f"{bright}{red}\n [+] {reset}{blue}Please use -h to get more information.")
            
        except argparse.ArgumentTypeError:
            print(f"{bright}{blue}\n [+] {reset}{blue}Please use -h to get more information.")
            
        except Exception as e:
            print(f"{bright}{red}\n [+] {reset}{blue}Unexpected Argument Error:{e}")
    
    def help(self):
        # Funtion to create and return the available options and flags.
        return f"""\n
    {bold}{white}[{reset}{bold}{blue}DESCRIPTION{reset}{white}]{reset}: {white}{bold}Cryptihub{reset} {white}is a CLI chat application by {reset}{bold}{green}Pevinkumar A{reset}.\n
        {bold}{white}[{reset}{bold}{blue}Usage{reset}{white}]{reset}: python3 {sys.argv[0]} \n
                {white}rootEsc {bold}{white}[{reset}{bold}{blue}Flags{reset}{bold}{white}]\n
        [{reset}{bold}{blue}Flags{reset}{bold}{white}]
                    
                [{reset}{bold}{blue}Filters{reset}{bold}{white}]{reset}
                
                    -nb,   --no-banner              :  It will disable the printing banner.
                        
                {bold}{white}[{reset}{bold}{blue}Debug{reset}{bold}{white}]{reset}
                    
                    -v,   --version                 :  To check version of this tool. 
                    -h,   --help                    :  To see all the available options.
            """
            
    def get_version(self):
        #funtion which is used to get the version (tag) from github through api.
        try:
            url="https://api.github.com/repos/PkTheHacker10/Cryptihub/releases/latest"
            response=requests.get(url,timeout=3,verify=True)
            if response.status_code==200:
                json_data=response.json()
                latest=json_data.get('tag_name')
                
                return "The Cryptihub tool is currently running in the version of " + latest 
            else:
                return "The Cryptihub tool is currently running in the version of v1.1"
            
        except (requests.ConnectTimeout,requests.ReadTimeout,requests.Timeout):
            print(f"{bright}{blue}\n [+] {reset} : Connection TimeOut while getting version.")
            
        except requests.JSONDecodeError:
            print(f"{bright}{red}\n [+] {reset} : Couldn't decode data.")
    