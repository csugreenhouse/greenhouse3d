import importlib
from pathlib import Path
import os
import pytest
from pytest import approx
import array
import cv2

apriltags_util = importlib.import_module("utils.apriltags")

def test_apriltag_detection():
    srcfour = "testfiles/fourtags.jpg"
    srcone = "testfiles/onetag.jpg"

    image4tag = cv2.imread(srcfour)
    image1tag = cv2.imread(srcone)

    taginfofour = apriltags_util.scan_apriltags(image4tag)
    taginfoone = apriltags_util.scan_apriltags(image1tag)

    assert len(taginfofour) == 4
    assert len(taginfoone) == 1

