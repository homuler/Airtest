import os
import json
import argparse
# import here to build dependent modules
from moa.moa import *
import g1utils
import g18utils
import sdkautomator


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", help="script filename")
    ap.add_argument("--utilfile", help="utils filepath to implement your own funcs")
    ap.add_argument("--setsn", help="auto set serialno", nargs="?", const=True)
    ap.add_argument("--setwin", help="auto set windows", action="store_true")
    ap.add_argument("--log", help="auto set log file", nargs="?", const="log.txt")
    ap.add_argument("--screen", help="auto set screen dir", nargs="?", const="img_record")
    ap.add_argument("--kwargs", help="extra kwargs")
    ap.add_argument("--forever", help="run forever, read stdin and exec", action="store_true")
    args = ap.parse_args()


    if args.forever:
        f = open("tmp", "w")
        while True:
            print "wait for stdin..."
            line = sys.stdin.readline()
            f.write(line)
            f.flush()
            exec(line) in globals()
            if line == "":
                print "end of stdin"
                exit(0)
            pass


    # loading util file
    if args.utilfile:
        if os.path.isfile(args.utilfile):
            print "try loading:", args.utilfile
            utilcontent = open(args.utilfile).read()
            exec(utilcontent) in globals()
        else:
            print "file does not exist:", os.path.abspath(args.utilfile)

    # cd script dir
    os.chdir(args.script)

    if args.setsn:
        print "auto set_serialno", args.setsn
        # if setsn==True, but not specified, auto choose one
        sn = args.setsn if isinstance(args.setsn, str) else None
        set_serialno(sn)

    if args.setwin:
        print "auto set_windows"
        set_windows()

    if args.log:
        print "save log in", args.log
        set_logfile(args.log)

    if args.screen:
        print "save img in", args.screen
        set_screendir(args.screen)

    if args.kwargs:
        print "load kwargs", repr(args.kwargs)
        for kv in args.kwargs.split(","):
            k, v = kv.split("=")
            globals()[k] = v

    # execute code
    exec_script(args.script, scope=globals())


if __name__ == '__main__':
    main()
