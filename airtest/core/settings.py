# encoding=utf-8

"""settings can be changed by user."""

DEBUG = False
ADDRESS = ('127.0.0.1', 5037)
LOGFILE = "log.txt"
SCREEN_DIR = "img_record"
BASE_DIR = '.'
SAVE_SCREEN = None
RESIZE_METHOD = None
SCRIPTHOME = None
SRC_RESOLUTION = []  # to be move to DEVICE
CVSTRATEGY = None
CVSTRATEGY_ANDROID = ["siftpre", "siftnopre", "tpl"]
CVSTRATEGY_WINDOWS = ["tpl", "siftnopre"]
FIND_INSIDE = None
FIND_OUTSIDE = None
WHOLE_SCREEN = False  # 指定WHOLE_SCREEN时，就默认截取全屏(而非hwnd窗口截图)
CHECK_COLOR = False  # 针对灰化按钮的情形，如果遇到彩色按钮-灰化按钮识别问题，打开即可
THRESHOLD = 0.6
THRESHOLD_STRICT = 0.7
STRICT_RET = True
CVINTERVAL = 0.5
OPDELAY = 0.1
TIMEOUT = 20
WINDOW_TITLE = None
FIND_TIMEOUT = 20
FIND_TIMEOUT_TMP = 3