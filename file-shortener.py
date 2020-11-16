import os

# input directory, with or without trailing slash
inputDirectory = "/path/to/folder"
# max filename length
maxFilenameLength = 120
# max directory name length
maxDirNameLength = 100
# enable actually changing the files?
enableFileDirModification = False

# must be a directory
if not os.path.isdir(inputDirectory):
    print("Input wasn't a directory, exiting")
    exit(1)

# get last character and remove trailing slash if necessary to standardize with os.walk() subdirectories
if inputDirectory[-1] == os.sep:
    print("Last character of directory is a slash, removing it")
    inputDirectory = inputDirectory[:-1]

# initialize counters
dirCounter = dirEditCounter = fileCounter = fileEditCounter = longestDirLength = longestFileLength = 0

# https://stackoverflow.com/questions/53123867/renaming-folders-and-files-while-os-walking-them-missed-some-files-after-chang
# process from the bottom up, rather top down, to prevent changing a directory before its child dirs + files
for dirpath, dirs, files in os.walk(inputDirectory, topdown=False):
    # iterate through files that are immediate children in the current dirpath
    for f in files:
        fileCounter += 1

        # get extension of file and string length without extension
        extension = f.split(".")[-1]
        lengthWithoutExtension = len(f) - 1 - len(extension)

        # update longestLength if necessary
        if lengthWithoutExtension > longestFileLength:
            longestFileLength = lengthWithoutExtension

        # if the length is longer than allowed, rename it to a shortened length, preserving extension
        if lengthWithoutExtension > maxFilenameLength:
            fileEditCounter += 1
            # create the shortened length filename
            renamedFile = f[0:maxFilenameLength] + "." + extension
            if enableFileDirModification:
                # perform the update to the file
                renameOutput = os.rename(os.path.join(dirpath, f), os.path.join(dirpath, renamedFile))

    dirCounter += 1

    # get the name of the current directory without parents
    closestDir = dirpath.split(os.sep)[-1]

    # update longestLength if necessary
    if len(closestDir) > longestDirLength:
        longestDirLength = len(closestDir)

    # if the length is longer than allowed, rename it to a shortened length
    if len(closestDir) > maxDirNameLength:
        dirEditCounter += 1

        # https://www.geeksforgeeks.org/join-function-python/
        # split the dirpath on separator to remove the current directory. Join back together with separator
        # Then append another separator and the current directory's shortened name
        dirpathWithoutClosestDir = os.sep.join(
            dirpath.split(os.sep)[0:len(dirpath.split(os.sep)) - 1]) + os.sep + closestDir[0:maxDirNameLength]

        if enableFileDirModification:
            # perform the update to the file
            os.rename(dirpath, dirpathWithoutClosestDir)

print("Directories scanned:", dirCounter, ", directories renamed:", dirEditCounter)
print("Files scanned:", fileCounter, ", files renamed:", fileEditCounter)
print("Longest directory name:", longestDirLength, ", longest filename while considering extension:", longestFileLength)
