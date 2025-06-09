try:
    from modules.core import CryptiHubCore
    from modules.cli.cli import CommandLine

except ImportError as Ie:
    print(f"Error [Server]: {Ie}")

def main() -> None:
    """
        Main function for the server to start the CryptiHub server.

        Args:
            None

        Returns:
            None
    """
    commandline = CommandLine()
    arguments = commandline.args()

    if not arguments.no_banner:
        print(commandline.get_banner())

    if arguments.help:
        print(commandline.get_help())
        exit()

    crypti_hub = CryptiHubCore()
    crypti_hub.start()

if __name__=="__main__":
    main()