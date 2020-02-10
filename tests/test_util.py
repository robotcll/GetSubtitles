# coding: utf-8

import os
from os import path
import copy
import shutil
import unittest
from collections import OrderedDict

from getsub.util import get_videos


class TestGetVideos(unittest.TestCase):

    test_dir = path.join(os.getcwd(), "TESTGETVIDEOS")
    test_dir_structure1 = {
        "sub1": ["file1.mkv", "file2", "file1.ass"],
        "sub2": ["fil3", "file4.mkv", "file4.zh.srt"],
        "file5.mkv": None,
        "storepath": ["file1.zh.ass", "file5.ass"],
    }
    file1_result = {
        "video_path": path.join(test_dir, "sub1"),
        "store_path": path.join(test_dir, "sub1"),
        "has_subtitle": True,
    }
    file4_result = {
        "video_path": path.join(test_dir, "sub2"),
        "store_path": path.join(test_dir, "sub2"),
        "has_subtitle": True,
    }
    file5_result = {
        "video_path": test_dir,
        "store_path": test_dir,
        "has_subtitle": False,
    }
    # test directory
    desired_result1 = {
        "file5.mkv": file5_result,
        "file1.mkv": file1_result,
        "file4.mkv": file4_result,
    }
    # test absolute path
    desired_result2 = {"file1.mkv": file1_result}
    desired_result3 = {"file5.mkv": file5_result}
    # test single video name
    desired_result4 = {"file5.mkv": file5_result.copy()}
    desired_result4["file5.mkv"]["video_path"] = "file5.mkv"
    desired_result4["file5.mkv"]["store_path"] = os.getcwd()
    # test store path
    test_dir_structure2 = copy.deepcopy(test_dir_structure1)
    test_dir_structure2["sub1"].remove("file1.ass")
    test_dir_structure2["sub2"].remove("file4.zh.srt")
    desired_result5 = copy.deepcopy(desired_result1)
    desired_result5["file4.mkv"]["has_subtitle"] = False
    desired_result5["file5.mkv"]["has_subtitle"] = True
    desired_result5["file1.mkv"]["store_path"] = path.join(
        test_dir, "storepath"
    )
    desired_result5["file4.mkv"]["store_path"] = path.join(
        test_dir, "storepath"
    )
    desired_result5["file5.mkv"]["store_path"] = path.join(
        test_dir, "storepath"
    )

    @classmethod
    def create_file(cls, path):
        with open(path, "w") as f:
            pass

    @classmethod
    def create_test_directory(cls, dir_structure):
        os.mkdir(cls.test_dir)
        for k, v in dir_structure.items():
            if v is None:  # file
                cls.create_file(path.join(cls.test_dir, k))
                continue
            os.mkdir(path.join(cls.test_dir, k))
            for f in v:
                cls.create_file(path.join(cls.test_dir, k, f))

    def tearDown(self):
        shutil.rmtree(TestGetVideos.test_dir)

    def test_directory(self):
        TestGetVideos.create_test_directory(TestGetVideos.test_dir_structure1)
        videos = get_videos(TestGetVideos.test_dir)
        self.assertDictEqual(
            videos, OrderedDict(TestGetVideos.desired_result1)
        )

    def test_absolute_video_path(self):
        TestGetVideos.create_test_directory(TestGetVideos.test_dir_structure1)
        videos = get_videos(
            path.join(TestGetVideos.test_dir, "sub1", "file1.mkv")
        )
        self.assertDictEqual(
            videos, OrderedDict(TestGetVideos.desired_result2)
        )
        videos = get_videos(path.join(TestGetVideos.test_dir, "file5.mkv"))
        self.assertDictEqual(
            videos, OrderedDict(TestGetVideos.desired_result3)
        )

    def test_single_video_name(self):
        TestGetVideos.create_test_directory(TestGetVideos.test_dir_structure1)
        videos = get_videos("file5.mkv")
        self.assertDictEqual(
            videos, OrderedDict(TestGetVideos.desired_result4)
        )

    def test_store_path(self):
        TestGetVideos.create_test_directory(TestGetVideos.test_dir_structure2)
        videos = get_videos(
            TestGetVideos.test_dir,
            store_path=path.join(TestGetVideos.test_dir, "storepath"),
        )
        print(videos)
        print(TestGetVideos.desired_result5)
        self.assertDictEqual(
            videos, OrderedDict(TestGetVideos.desired_result5)
        )


if __name__ == "__main__":
    unittest.main()