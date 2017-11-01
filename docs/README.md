Airtest
================

Automated Testing Framework

## Getting Started

Airtest is an automated testing framework with main focus on games, however it can be used for other native applications as well. Currently, Windows and Android operating systems are supported. Support for iOS comes in near future.

Airtest framework is based on image recognition technology and provides cross-platform APIs that allows to install application, perform simulated input, make assertions, and so forth. It also generates the report when testing is finished.

**AirtestIDE** is an out of the box GUI tool that helps to create and record test cases in the user-friendly way. AirtestIDE provides QA with entire production workflow: ``record -> replay -> report``


## Installation

This section describes how to install Airtest test framework.

**System Requirements**

* Operating System: 
  * Windows
  * MacOS X
  * Linux

* Python2.7 & Python3.3+

**Installing the python package**

Airtest package can be installed directly from Git repository. Use ``pip`` to
to manage installation of all dependencies and package itself.

```Shell
git clone ssh://git@git-qa.gz.netease.com:32200/gzliuxin/airtest.git
pip install -e airtest
```

Use `-e` here to install airtest in develop mode since this repo is in rapid development. Then you can upgrade the repo with `git pull` later.

**Using samples**

Airtest also contains the samples using this library in several scenarios. All samples can be found in `playground` directory in cloned repository.

## Using as python package

Airtest provides simple APIs that are platform independent. This section describes how to create simple API-specific test scenario which does the following:
 
1. connects to local android device with `adb`
1. installs the `apk` application
1. runs application and takes the screenshot
1. performs several user operations (touch, swipe, keyevent)
1. uninstalls application

```Python
from airtest.core.main import *

# connect to local device with adb
connect_device("Android:///")

# start your script here
install("path/to/your/apk")
start_app("package_name_of_your_apk")
snapshot()
touch((100, 100))
touch("image_of_a_button.png")
swipe((100, 100), (200, 200))
swipe("button1.png", "button2.png")
keyevent("BACK")
home()
uninstall("package_name_of_your_apk")
```
Please refer to full [Airtest Python API reference](./all_module/airtest.core.api.html) for more detailed info.

## Running from command line interface

Airtest can be run from command line interface as well. All test cases, test code and image templates must be placed in one directory with `.owl` suffix. The easiest way to create and record the test cases is to use GUI **Airtest IDE**.

The biggest advantage of using the Airtest CLI is the possibility to execute the test cases and test scenarios on different host machine without using IDE itself. Connections to devices are specified by command line arguments, i.e. the test code is platform independent and one code, test cases, scenarios can be used for Android, Windows or iOS devices as well. 

Following examples demonstrate the basic usage of airtest framework from CLI. For more detailed info, refer to provided samples of test cases and code: ```airtest/playground/test_blackjack.owl/```


### run test case
````Shell
# run test test cases and scenarios on various devices
> python -m airtest run <path to your owl dir> --device Android:///
> python -m airtest run <path to your owl dir> --device Android://adbhost:adbport/serialno
> python -m airtest run <path to your owl dir> --device Windows:///
> python -m airtest run <path to your owl dir> --device iOS:///
...
# show help
> python -m airtest run -h
usage: __main__.py run [-h] [--device [DEVICE]] [--log [LOG]]
                       [--kwargs KWARGS] [--pre PRE] [--post POST]
                       script

positional arguments:
  script             owl path

optional arguments:
  -h, --help         show this help message and exit
  --device [DEVICE]  connect dev by uri string, e.g. Android:///
  --log [LOG]        set log dir, default to be script dir
  --kwargs KWARGS    extra kwargs used in script as global variables, e.g.
                     a=1,b=2
  --pre PRE          owl run before script, setup environment
  --post POST        owl run after script, clean up environment, will run
                     whether script success or fail
````


### generate html report
```Shell
> python -m airtest report <path to your owl directory>
log.html
> python -m airtest report -h
usage: __main__.py report [-h] [--outfile OUTFILE] [--static_root STATIC_ROOT]
                          [--log_root LOG_ROOT] [--gif [GIF]]
                          [--gif_size [GIF_SIZE]] [--snapshot [SNAPSHOT]]
                          [--record RECORD [RECORD ...]]
                          [--new_report [NEW_REPORT]]
                          script

positional arguments:
  script                script filepath

optional arguments:
  -h, --help            show this help message and exit
  --outfile OUTFILE     output html filepath, default to be log.html
  --static_root STATIC_ROOT
                        static files root dir
  --log_root LOG_ROOT   log & screen data root dir, logfile should be
                        log_root/log.txt
  --gif [GIF]           generate gif, default to be log.gif
  --gif_size [GIF_SIZE]
                        gif thumbnails size (0.1-1), default 0.3
  --snapshot [SNAPSHOT]
                        get all snapshot
  --record RECORD [RECORD ...]
                        add screen record to log.html
  --new_report [NEW_REPORT]

```


### get test case info
```Shell
# get test case info in json, including: author, title, desc
> python -m airtest info <path to your owl directory>
{"author": ..., "title": ..., "desc": ...}
```