## Airtest开源项目

自动化测试框架

*	基于图像匹配，适合做游戏的自动化测试，同样也可以用作App
*	支持Windows/Android/iOS
*	提供[IDE](http://init.nie.netease.com/airtest_home/)，0上手成本，支持完整的工作流程：录制、回放、生成报告
*	同样作为Python库，可以用作其他测试框架的底层，提供跨平台的模拟操作、断言、报告生成等功能

## Development
1. 安装aircv
git clone -b open-source ssh://git@git-qa.gz.netease.com:32200/airtest-projects/aircv.git
pip install -e aircv
1. 安装airtest
git clone ssh://git@git-qa.gz.netease.com:32200/gzliuxin/airtest.git
pip install -e airtest


## Use as a python package
```
from airtest.core.main import *

# init a android device, adb connection required
set_serialno()

# start your script here
aminstall("path/to/your/apk")
amstart("package_name_of_your_apk")
snapshot()
touch((100, 100))
touch("picture_of_a_button.png")
swipe((100, 100), (200, 200))
keyevent("BACK")
home()
uninstall("package_name_of_your_apk")
```


## 命令行工具
因为脚本中包含图片资源，所以我们设计了.owl的目录结构，用IDE可以方便地录制.owl脚本。为了不依赖IDE运行脚本，同时支持跨平台运行，我们提供了命令行工具：将设备初始化、配置等平台相关操作用命令行参数传入，脚本中只包含平台无关的操作逻辑和断言。

使用方法参考:

> python -m airtest -h
// 运行脚本
> python -m airtest run
// 生成报告
> python -m airtest report
// 获取脚本信息
> python -m airtest info


## 基本接口说明

### set\_serialno(sn=None)

	设置手机的序列号, 支持*匹配。如果adb连接了多台手机，默认取第一台

		set_serialno('cff*')
		
### set\_ios\_udid(udid=None)

	设置ios device的序列号, 支持*匹配。如果usb连接了多台手机，默认取第一台

		set_ios_udid('cff*')

### set\_basedir(base\_dir)

	设置你的工作目录，日志，图片都会以这个基准去查找

### set\_logfile(filename, inbase=True)

	设置日志文件的路径，如果inbase为true的话，日志会保存到basedir目录下

### set_scripthome(dirpath)
	
	设置脚本根目录，用于exec_script

### set_globals(key, value)
	设置moa里面的一些全局变量


### log(tag, data)

	data一定是需要json.dumps支持的格式才行.

### shell(cmd, shell=True)

	执行shell命令，然后返回

		print shell('echo hello')
		# output: hello

### amstart(package)	
>*android only( add adaptation for ios device, package is appid)*

	am: android manager的简称

		amstart('com.netease.moa') # 启动应用

### amstop(package)
>*android only( add adaptation for ios device, package is appid)*

	强制停止应用，等同于`am force-stop <package>`

### amclear(package)
>*android only*

	清空应用中的数据，等同于`pm clear <package>`

### install(filepath)
>*android only( add adaptation for ios device)*

	安装apk

### uninstall(package)
>*android only( add adaptation for ios device)*

	卸载apk

### snapshot(filename="screen.png")

	保存手机上的截图到filename这个文件。然后返回图像的二进制内容

### wake()
>*android only*

	点亮手机屏幕

### home()
>*android only*

	点击手机home键

### touch(v, timeout=TIMEOUT, delay=OPDELAY, offset=None, safe=False)

	点击屏幕中的目标，参数如下：

		v 目标，有三种形态：坐标、图片、文字，详见MoaPic

		timeout 超时时间

		delay 操作后延迟时间

		offset 点击坐标偏移，可以是坐标或者是屏幕百分比。offset={"percent": True, "x": 20, "y": 20}

		safe 没找到图片是否忽略错误，默认False，会报MoaError

### swipe(v1, v2=None, vector=None)

	滑动操作，两种形态：

		swipe(v1, v2) 从起点目标滑动到终点目标

		swipe(v1, vector=(x, y)) 从起点目标滑动一个向量。vector=(dx/w, dy/h)

### operate(v, route, timeout=TIMEOUT, delay=OPDELAY)

	长操作，在起点处按下，按照一个线路滑动，最终松开

		v 起点目标

		route 滑动线路 [(dx1, dy1, dt1), (dx2, dy2, dt2), (dx3, dy3, dt3)...]  其中(dx, dy)与swipe参数vector相同
		
		timeout 同上
		
		delay 同上

### keyevent(keyname)
	
	按键输入

		keyname 安卓参考：http://developer.android.com/reference/android/view/KeyEvent.html

	注意：windows按键和android按键不同

### text(text)
	
	文字输入

	注意：windows可以输入中文，android暂时不行

### sleep(secs=1.0)

	等待时间

### wait(v, timeout=10, safe=False, interval=CVINTERVAL, intervalfunc=None)

	等待目标出现

		v 目标

		timeout 超时时间

		safe 超时是否继续，默认为False即会报错

		interval 等待目标的间隔时间

		intervalfunc 等待目标的间隔中的回调函数

### exists(v, timeout=1)

	判断目标是否存在，返回True/False

### assert_exists(v, msg="", timeout=TIMEOUT)
	
	断言目标存在，如果超时时间内不存在则抛出AssertionError

		v 目标

		msg 断言信息

		timeout 超时时间

### assert_not_exists(v, msg="", timeout=2)

	断言目标不存在，如果超时时间内存在则抛出AssertionError，参数同上

### assert_equal(first, second, msg="")
	
	断言first和second相等，不等则抛出AssertionError



### MoaPic(filename, rect=None, threshold=THRESHOLD, target_pos=TargetPos.MID, record_pos=None, resolution=[])
	
	一个隐藏的类，所有图片目标在moa中都会转换为MoaPic实例，参数如下：
		filename	图片名
		rect		所在区域(x0, y0, x1, y1)，默认全屏，不建议给这个参数
		threshold	识别阈值，默认阈值为0.6，较低，可以按需修改
		target_pos	目标图片的点击位置，默认点击目标中点，可以填1-9表示不同位置，小键盘排布
		record_pos	记录下的录制坐标，用于辅助图像识别
		resolution	记录下的屏幕分辨率，用于辅助图像识别
