import os
import ctypes
import Database

def main():
    PATH_TO_DATA = os.path.join(os.getcwd(), 'data')
    database = Database(os.path.join(os.getcwd(), 'database', 'db.csv'))

    for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
        for f in filenames:
            fName = os.path.join(dirpath, f)
            process(fName, database)

# http://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
def is_hidden(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    return name.startswith('.') or has_hidden_attribute(filepath)

# http://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
def has_hidden_attribute(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    
    return result

main()
