import time
import datetime
import os
import psutil

import notification

from typing import *


def list_all_proc(conf, keywords: List[str]) -> None:
    """
    List all processes of the current user.
    """

    current_user = os.getlogin()

    my_procs = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(
                attrs=["pid", "name", "username", "status", "create_time", "cmdline"]
            )

            # Check if the process is owned by the current user.
            if pinfo["username"] != current_user:
                continue

            # Check if the process is running.
            if pinfo["status"] != psutil.STATUS_RUNNING:
                continue

            # Check if the process name contains one of the keywords.
            for keyword in keywords:
                if keyword in pinfo["name"]:
                    my_procs.append(pinfo)
                    break

        except psutil.NoSuchProcess:
            pass

    if len(my_procs) < 1:
        print("No my process found.")
        return

    msg = dict()
    msg["title"] = "List of My Processes"
    msg["content"] = "I have {} processes.\n\n".format(len(my_procs))
    for proc in my_procs:
        msg["content"] += "- Pid {} of {} started at {}:\n".format(
            proc["pid"],
            proc["name"],
            datetime.datetime.fromtimestamp(proc["create_time"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )
        cmdline_str = " ".join(proc["cmdline"])
        msg["content"] += "--  its command: {}\n\n".format(cmdline_str)
    notification.notify(conf, msg)


def check(conf):
    print("[{}] Start checking processes.".format(datetime.datetime.now()))

    proc_conf = conf["proc"]

    if proc_conf["list_all_proc"]:
        print("List all my processes.")
        list_all_proc(conf, proc_conf["my_proc_keywords"])
    else:
        print("Do not list all my processes.")

    pids = proc_conf["mon"]

    if len(pids) >= 1:
        print("There are processes to check.")
        not_running = []
        for pid in pids:
            if not psutil.pid_exists(pid):
                not_running.append(pid)

        if len(not_running) >= 1:
            msg = dict()
            msg["title"] = "Process Ended"
            msg["content"] = ",".join([str(e) for e in not_running])
            msg["content"] += " is/are not running now."
            notification.notify(conf, msg)
