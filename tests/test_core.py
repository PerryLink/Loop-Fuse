import pytest
from loop_fuse.core import LoopFuse
from loop_fuse.exceptions import LoopDetectedError

def test_basic_loop_detection():
    """测试基础循环检测"""
    fuse = LoopFuse(window_size=5, threshold=3)

    fuse.monitor("action1")
    fuse.monitor("action1")

    with pytest.raises(LoopDetectedError):
        fuse.monitor("action1")

def test_window_size():
    """测试滚动窗口"""
    fuse = LoopFuse(window_size=3, threshold=2)

    fuse.monitor("a")
    fuse.monitor("b")
    fuse.monitor("c")
    fuse.monitor("a")

    with pytest.raises(LoopDetectedError):
        fuse.monitor("a")

def test_different_actions():
    """测试不同操作不触发"""
    fuse = LoopFuse(threshold=3)

    fuse.monitor("action1")
    fuse.monitor("action2")
    fuse.monitor("action3")
    fuse.monitor("action4")
