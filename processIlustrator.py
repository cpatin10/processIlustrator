#!/usr/bin/python3

import os

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', 
                        action='store_true',
                        help='Detect proccess.')
    arguments = parser.parse_args()
    return arguments

def main():
    try:
        if os.name != 'posix':
            raise Exception('This programm is only for Linux.')
        arguments = parseArgs()
        path = '/proc'
        procDir = os.listdir(path)
    except Exception as e:
        print (e)

if __name__  == "__main__":
    main()
