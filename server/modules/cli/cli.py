try:
    import argparse
    from colorama import Fore,Style 

    red = Fore.RED
    blue = Fore.BLUE
    white = Fore.WHITE
    magenta = Fore.MAGENTA
    bright = Style.BRIGHT
    green = Fore.GREEN
    red = Fore.RED
    bold = Style.BRIGHT
    yellow = Fore.YELLOW
    cyan = Fore.CYAN
    mixed = Fore.BLUE+Fore.GREEN+Fore.RED
    reset = Style.RESET_ALL
    
except ImportError as Ie:
    print(f"Error [Core]: {Ie}")

class CommandLine:
    """
        Class to handle cli operations.

        Args:
            None

        Returns:
            None
    """
    def get_banner(self) -> str:
        """
            Function to get the banner.

            Args:
                None

            Returns:
                str: Returns the banner for cryptihub.
        """
        banner = """
              _____              __  _ __ __     __ 
             / ___/_____ _____  / /_(_) // /_ __/ / 
            / /__/ __/ // / _ \\/ __/ / _  / // / _ \\
            \\___/_/  \\_, / .__/\\__/_/_//_/\\_,_/_.__/
                    /___/_/                            V1.0.0
                                                

            This is a Python based E2EE-lite Group chat
        """

        return banner
    
    def args(self) -> list:
        """
            Function to define arguments.

            Args:
                None

            Returns:
                list: Returns the list of arguments. 
        """
        parser = argparse.ArgumentParser(add_help = False,usage = argparse.SUPPRESS,exit_on_error = False)
        try:
            parser.add_argument("-nb","--no-banner",action="store_true")
            parser.add_argument("-h","--help",action="store_true")
            
            args = parser.parse_args()
            return args
        
        except argparse.ArgumentError:
            print(f"{bright}{red}\n [+] {reset}{blue}Please use -h to get more information.")
            
        except argparse.ArgumentTypeError:
            print(f"{bright}{blue}\n [+] {reset}{blue}Please use -h to get more information.")
            
        except Exception as e:
            print(f"{bright}{red}\n [+] {reset}{blue}Unexpected Argument Error:{e}")
    
    def get_help(self) -> str:
        """
            Function to get help menu.

            Args:
                None

            Returns:
                str: Returns the help menu.
        """
        return f"""
    {bold}{white}[{reset}{bold}{blue}DESCRIPTION{reset}{white}]{reset}: {white}{bold}Cryptihub{reset} {white}is a GUI chat application by {reset}{bold}{green}Pevinkumar A{reset}.\n
        {bold}{white}[{reset}{bold}{blue}Usage{reset}{white}]{reset}: python3 server.py \n
                {white}rootEsc {bold}{white}[{reset}{bold}{blue}Flags{reset}{bold}{white}]\n
        [{reset}{bold}{blue}Flags{reset}{bold}{white}]
                    
                [{reset}{bold}{blue}Filters{reset}{bold}{white}]{reset}
                
                    -nb,  --no-banner           :  It will disable the printing banner.
                        
                {bold}{white}[{reset}{bold}{blue}Debug{reset}{bold}{white}]{reset}
                    
                    -h,  --help                 :  To see all the available options.

                {bold}{white}[{reset}{bold}{blue}Server commands{reset}{bold}{white}]{reset} (Need to run the server)

                        /help                   : To see available commands.           
                        /users                  : To see all the users in the chat.    
                        /stop                   : To stop the server. 
            """
    