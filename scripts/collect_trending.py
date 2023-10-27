import argparse
from pathlib import Path
from trending import createJSON

def getPath(fname):
    path = Path(__file__).parent / fname
    return path

def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output",help="Name of the output file")
    return parser.parse_args()

def main():
    args = argumentParser()
    
    createJSON(args.output)

if __name__ == "__main__":
    main()
