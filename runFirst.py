""" Run when you first download this package and it will download and process all the files you need """
import download
import process

def main():
    setup()

def setup():
    download.main()
    process.main() 

if __name__ == '__main__': main()
