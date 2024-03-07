# load environment variables as early as possible in your script
from dotenv import load_dotenv

load_dotenv()


def main():
    # if is authenticated, display index page
    # else, show login page
    pass


if __name__ == "__main__":
    main()
