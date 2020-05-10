## Python File Shortener

Background

* I have files on a macOS computer. I transfer them using SMB to a NAS running Unraid. I then access them and move them around using Windows 10, also connected to Unraid with SMB. Windows, however, often throws errors when accesing the files when it complains about file or path length. It appears macOS and Unraid allow longer path and file lengths than on Windows. 
* In experience, I have seen filenames created by macOS with 255 characters, and directory names in excess of 100 characters. This does not count the absolute path length, which is then often times 350 or even 400 characters. 
* Meanwhile, Windows appears to have a path length limit of 255, and it cannot even edit these files to make them shorter



Solution

* This Python script's first few lines take in the max directory length and filename length, as well as the directory to look inside and if we want to do a dry-run or actually destructively edit the files' names
* The script uses Python 3.7's built-in `os` library and its `walk()` function to recursively iterate through all files under a certain directory. It then uses string and array manipulation to edit the directory or file names, and again uses the `os` library to `rename()` to the shorter length
* The script performs all the modifications and then prints out a summary of files scanned and files edited, as well as the max directory name length and file name length it experienced
* My macOS computer with an NVMe SSD was able to process 40,000 small files and 2,000 directories in around one second. 



Challenges

* The default behavior of the `walk()` function is to work from the topmost directory downwards. However, since we're modifying directory names and thus changing the path while it is also trying to read the path, this approach does not work. Instead, we must work from the very deepest directory and go outwards from there.
* Additionally, we must edit the files in a directory before we edit the directory itself. That is why we edit and update the files before updating the current directory