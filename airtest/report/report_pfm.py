#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
import traceback
import time
from collections import defaultdict


def gen_pfm_json(log_path):
    """
    检查log文件夹下是否有符合格式的性能数据log文件，如果有就生成对应的Json文件
    Parameters
    ----------
    log_path

    Returns
    -------

    """
    log_pattern = r"pfm_?(?P<serialno>\w*).txt"
    ret = []
    devices = []
    trace_list = []

    for f in os.listdir(log_path):
        f_match = re.match(log_pattern, f)
        if not f_match:
            continue
        serialno = f_match.groupdict()['serialno']
        devices.append(serialno)
        data, trace = trans_log_json(os.path.join(log_path, f))
        data["serialno"] = serialno
        ret.append(data)
        if trace:
            trace_list.extend(trace)
    # 如果存在额外文件，读取数据放入json中
    if os.path.exists(os.path.join(log_path, "fps.txt")):
        extra_data = read_extra_data(os.path.join(log_path, "fps.txt"))
        if extra_data and ret:
            ret[0]["extra_data"] = extra_data
    if not ret:
        return [], [], ""
    content = "json_data=" + json.dumps(ret)
    output = os.path.join(log_path, "pfm_local.json")
    try:
        with open(output, "w+") as f:
            f.write(content)
        with open(os.path.join(log_path, "pfm.json"), "w+") as f:
            f.write(json.dumps(ret))
    except:
        print(traceback.format_exc())
        return [], [], ""
    return devices, trace_list, log_path


def trans_log_json(log="pfm.txt"):
    """
    把运行中生成的log文件生成json格式，并且进行一定的处理
    Parameters
    ----------
    log

    Returns 解析出来的数据和traceback内容
    -------

    """
    data = defaultdict(lambda: defaultdict(lambda: 0))
    ret = {"cpu": [], "pss": [], "net_flow": [], "cpu_freq": {},
           "keys": ["cpu", "pss", "net_flow"],
           "title": log, "cpu_freq_data": {}}
    times = []
    transback_content = []
    func_dict = {
        "cpu": cpu,
        "pss": pss,
        "net_flow": net_flow,
        "cpu_freq": cpu_freq,
    }
    with open(log) as f:
        for item in f.readlines():
            item = json.loads(item)
            if item["name"] == "traceback":
                transback_content.append(item["value"])
                continue
            try:
                t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(item["time"])))
            except:
                t = item["time"]
            try:
                if item["value"] != "":
                    value = json.loads(item["value"])
                    data[t][item["name"]] = func_dict[item["name"]](value) if item["name"] in func_dict else value
                else:
                    data[t][item["name"]] = ""
            except:
                data[t][item["name"]] = 0
            if t not in times:
                times.append(t)

    for t in times:
        for k in func_dict.keys():
            if k != 'cpu_freq':
                ret[k].append(data[t][k])
            elif data[t]["cpu_freq"]:
                for kernel, freq in data[t]["cpu_freq"].items():
                    if kernel not in ret["cpu_freq"]:
                        ret["cpu_freq"][kernel] = [freq]
                    else:
                        ret["cpu_freq"][kernel].append(freq)
    ret["times"] = times
    return ret, transback_content


def read_extra_data(filename="fps.txt"):
    """
    临时增加的新接口，用于读取引擎自己写的数据内容，格式比较固定
    第一行为 生成的task id，从第二行开始是写入的数据
    Parameters
    ----------
    filename

    Returns {"times": [], "fps": [], "tag": []}
    -------

    """
    if not os.path.exists(filename):
        return []

    task_id = 0
    fps_data = None
    ret = defaultdict(list)
    with open(filename, "r") as f:
        for line in f.readlines():
            data = json.loads(line)
            if isinstance(data, int) or isinstance(data, str):
                task_id = data
            else:
                fps_data = data
    if fps_data:
        for item in fps_data:
            ret["times"].append(item["time"])
            for k, v in item["data"].items():
                ret[k].append(v)
        if ret["tag"]:
            tag = ret["tag"][0]
            tag_index_list = [0]
            for i, t in enumerate(ret["tag"]):
                if t != tag:
                    tag_index_list.append(i)
                    tag = t
            ret["tag_list"] = tag_index_list
        return ret
    else:
        return None


def cpu(value):
    return round(float(value), 2)


def pss(value):
    """
    内存的单位是KB，转为MB
    Parameters
    ----------
    value pss kb

    Returns pss/1024
    -------

    """
    return round(float(value)/1024.0, 2)


def net_flow(value):
    """
    流量，输入值为 n B/s
    Parameters
    ----------
    value 当前流量值 B/S

    Returns 流量值KB/S
    -------

    """
    return round(float(value)/1024.0, 2)


def cpu_freq(value):
    """

    Parameters
    ----------
    value

    Returns
    -------

    """
    return value


def cpu_kernel(value):
    """
    计算活跃CPU核心数
    Parameters
    ----------
    value

    Returns
    -------

    """
    count = 0
    if isinstance(value, dict):
        for i in value.values():
            if i != "0" and i != 0:
                count += 1
        return count
    else:
        return 1