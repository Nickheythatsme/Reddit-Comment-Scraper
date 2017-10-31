import threading
import os
import sys
import tarfile

def get_file_out_name(directory):
    parts = directory.split('/')
    if len(parts[-1]) == 0:
        file_out = parts[-2] 
    else:
        file_out = parts[-1]
    return file_out + '.tar.gz'


def compress(directory_name):
    file_out = get_file_out_name(directory_name)
    print("Reading files from: {}".format(directory_name))
    print("Writing to: {}".format(file_out))
    tout = tarfile.open(name=file_out, mode='w:gz')
    tout.add(directory_name, recursive=True)
    tout.close()
    return


def main():
    threads = []
    for obj in sys.argv[1:]:
        print("Starting thread for: {}".format(obj))
        t = threading.Thread(name=obj, target=compress, args=(obj,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
        print("Thread finished: {}".format(t.name))


main()
