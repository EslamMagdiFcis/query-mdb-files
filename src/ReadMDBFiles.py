import os
import glob


def ReadMDBFiles(directory):
    MDBFiles = {}
    path = "{dir}*.mdb".format(dir=directory)
    for file in glob.glob(pathname=path):
        fileName = os.path.splitext(os.path.basename(file))[0]
        MDBFiles[fileName] = os.path.abspath(file)

    return MDBFiles
