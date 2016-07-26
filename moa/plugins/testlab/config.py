# encoding=utf-8


STF_HOST_IP = '192.168.40.111'
STF_TOKEN_ID = 'bfa446e605ba4af8b0d14487b257435e3b06722aace84de09faffc7119302050'


# 安装之前会先清掉第三方应用
# 这里是不清掉的列表
PKG_NOT_REMOVE = [
    # mtl保留应用
    "com.zj.deviceinfo",
    "com.tencent.mm",
    "com.finalwire.aida64",
    # testlab保留应用
    "com.netease.releaselock",
    "com.netease.accessibility",
    "com.github.uiautomator.test",
    "com.github.uiautomator",
    "jp.co.cyberagent.stf.rotationwatcher",
    "jp.co.cyberagent.stf",
    "jp.jun_nama.test.utf7ime",
    "com.android.adbkeyboard",
    # 保留的游戏app
    "com.netease.my",
]


# MTL提供的稳定设备列表
TEST_DEVICE_LIST = (
    '07173333',
    'QLXBBBA5B1137702',
    'JTJ4C15710038858',
    'T3Q4C15B04019605',
    '96528427',
    '1197d597',
    '4c6a4cf2',
    '351BBJPTHLR2',
    '351BBJPZ8F27',
    '351BBJPYF7PF',
    '88MFBM72H9SN',
    '810EBM535P6F',
    'BH904FXV16',
    'CB5A21QQEN',
    '4a139669',
    'T7G5T15730003758',
    'DU2SSE15CA048623',
    'DU2SSE149G047150',
    '71MBBLA238NH',
    '4df74f4b47e33081',
    'eebcdab5',
    '7N2SQL151N004298',
    'G1NPCX069194A8V',
    '4e49701b',
    '4d00df1f9b034067',
    '5T2SQL154G012154',
    'd523384',
    '0b2b5e3c',
    '8d95c245',
    '0815f8485f032404',
    '79AEALB253QE',
    'G2W7N15930015071',
    '02c1957e',
    'b0992898',
    'DU2SSE149G047150',
)