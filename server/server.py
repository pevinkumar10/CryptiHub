try:
    from modules.core import CryptiHubCore

except ImportError as Ie:
    print(f"Error [Server]: {Ie}")

def main():
    crypti_hub=CryptiHubCore()
    crypti_hub.start()

if __name__=="__main__":
    main()