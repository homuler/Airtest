# encoding=utf-8
from airtest.core.android.adb import ADB, AdbError, AdbShellError, DeviceConnectionError
from testconf import IMG, try_remove
from types import GeneratorType
import os
import unittest
import subprocess


class TestADBWithoutDevice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.adb = ADB()

    def test_adb_path(self):
        self.assertTrue(os.path.exists(self.adb.builtin_adb_path()))

    def test_start_server(self):
        self.adb.start_server()

    def test_version(self):
        self.assertIn("1.0.39", self.adb.version())

    def test_other_adb_server(self):
        adb = ADB(server_addr=("localhost", 5037))
        self.assertIn("1.0.39", adb.version())

    def test_start_cmd(self):
        proc = self.adb.start_cmd("devices", device=False)
        self.assertIsInstance(proc, subprocess.Popen)
        self.assertIsNotNone(proc.stdin)
        self.assertIsNotNone(proc.stdout)
        self.assertIsNotNone(proc.stderr)
        out, err = proc.communicate()
        self.assertIsInstance(out, str)
        self.assertIsInstance(err, str)

    def test_cmd(self):
        output = self.adb.cmd("devices", device=False)
        self.assertIsInstance(output, unicode)

        with self.assertRaises(AdbError):
            self.adb.cmd("wtf", device=False)

    def test_devices(self):
        all_devices = self.adb.devices()
        self.assertIsInstance(all_devices, list)


class TestADBWithDevice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        devices = ADB().devices(state="device")
        if not devices:
            raise RuntimeError("At lease one adb device required")
        cls.adb = ADB(devices[0][0])

    def test_devices(self):
        online_devices = self.adb.devices(state=self.adb.status_device)
        self.assertEqual(online_devices[0][0], self.adb.serialno)
        self.assertEqual(online_devices[0][1], self.adb.status_device)

    def test_get_status(self):
        self.assertEqual(self.adb.get_status(), self.adb.status_device)

    def test_wait_for_device(self):
        self.adb.wait_for_device()

        with self.assertRaises(DeviceConnectionError):
            ADB("some_impossible_serialno").wait_for_device(timeout=2)

    def test_start_shell(self):
        proc = self.adb.start_shell("time")
        self.assertIsInstance(proc, subprocess.Popen)
        out, err = proc.communicate()
        self.assertIsInstance(out, str)
        self.assertIsInstance(err, str)

    def test_raw_shell(self):
        output = self.adb.raw_shell("pwd")
        self.assertEqual(output.strip(), "/")
        self.assertIsInstance(output, unicode)

        self.assertIsInstance(self.adb.raw_shell("pwd", ensure_unicode=False), str)

    def test_shell(self):
        output = self.adb.shell("time")
        self.assertIsInstance(output, unicode)

        with self.assertRaises(AdbShellError):
            self.adb.shell("ls some_imposible_path")

    def test_getprop(self):
        output = self.adb.getprop("wifi.interface")
        self.assertIsInstance(output, unicode)

    def test_sdk_version(self):
        output = self.adb.sdk_version
        self.assertIsInstance(output, int)

    def test_exists_file(self):
        self.assertTrue(self.adb.exists_file("/"))

    def test_push(self):
        tmpdir = "/data/local/tmp"
        imgname = os.path.basename(IMG)
        tmpimgpath = os.path.join(tmpdir, imgname)
        self.adb.push(IMG, tmpdir)
        self.assertTrue(self.adb.exists_file(tmpimgpath))

    def test_pull(self):
        tmpdir = "/data/local/tmp"
        imgname = os.path.basename(IMG)
        tmpimgpath = os.path.join(tmpdir, imgname)
        self.adb.push(IMG, tmpdir)

        try_remove(imgname)
        self.adb.pull(tmpimgpath, ".")
        self.assertTrue(os.path.exists(imgname))
        try_remove(imgname)

    def test_get_forwards(self):
        self.adb.remove_forward()
        self.adb.forward(local='tcp:6100', remote="tcp:7100")

        forwards = self.adb.get_forwards()
        self.assertIsInstance(forwards, GeneratorType)

        forwards = list(forwards)
        self.assertEqual(len(forwards), 1)
        sn, local, remote = forwards[0]
        self.assertEqual(sn, self.adb.serialno)
        self.assertEqual(local, 'tcp:6100')
        self.assertEqual(remote, 'tcp:7100')

    def test_remove_forward(self):
        self.adb.remove_forward()
        self.assertEqual(len(list(self.adb.get_forwards())), 0)

        # set a remote and remove it
        self.adb.forward(local='tcp:6100', remote="tcp:7100")
        self.adb.remove_forward(local='tcp:6100')
        self.assertEqual(len(list(self.adb.get_forwards())), 0)

    def test_logcat(self):
        line_cnt = 0
        for line in self.adb.logcat():
            self.assertIsInstance(line, str)
            line_cnt += 1
            if line_cnt > 3:
                break
        self.assertGreater(line_cnt, 0)

if __name__ == '__main__':
    unittest.main()
