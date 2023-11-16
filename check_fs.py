import datetime
import os
import pwd

import notification


def check_dir(dir,exts, file_max, line_max):
    print("Checking dir {}.".format(dir))


    # get all files with extension name exts in dir
    files = []
    for ext in exts:
        files.extend([os.path.join(dir, f) for f in os.listdir(dir) if f.endswith(ext)])

    if len(files) < 1:
        print("No files to check.")
        return 'No files available.'

    # sort files by last modified time and takes file_max files
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    files = files[:file_max]

    if len(files) < 1:
        print("No files to check.")
        return 'No files available.'

    # must have been modified in the last 24 hours
    files = [f for f in files if os.path.getmtime(f) > datetime.datetime.now().timestamp() - 86400]

    if len(files) < 1:
        print("No files to check.")
        return 'Files not modified in the last 24 hours.'

    message = ''

    for file in files:
        # get last line_max lines
        lines = []
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = lines[-line_max:]

        if len(lines) < 1:
            continue

        message += "File {}:\n".format(file)
        message += ''.join(lines)
        message += '\n'

    return message



def check(conf):
    print("[{}] Start checking filesystem.".format(datetime.datetime.now()))

    proc_conf = conf["fs"]

    dirs = proc_conf["mon"]

    if len(dirs) < 1:
        print("No directory to check")
        return

    print("There are {} dirs to check.".format(len(dirs)))

    exts = proc_conf["exts"]
    
    if len(exts) < 1:
        print("No exts set. Default to .log")
        exts = [".log"]
    
    message = ''
    for dir in dirs:
        message += "Logs in dir {}:\n".format(dir)
        message += check_dir(dir,exts, proc_conf["lim_file"], proc_conf["lim_line"])
        
    msg = dict()
    msg["title"] = "Filesystem Report"
    msg["content"] = message
    notification.notify(conf,msg)


if __name__ == "__main__":
    print(check_dir('/home/xkz/UnsupGeotrans',[".log"], 3, 10))
