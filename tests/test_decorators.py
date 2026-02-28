import pytest
from loop_fuse.decorators import loop_fuse
from loop_fuse.exceptions import LoopDetectedError

def test_decorator_basic():
    """测试装饰器基础功能"""
    @loop_fuse(threshold=2)
    def my_func(action):
        return action

    my_func("test")

    with pytest.raises(LoopDetectedError):
        my_func("test")

def test_decorator_with_callback():
    """测试装饰器回调"""
    callback_called = []

    def callback(history, fp, cost):
        callback_called.append(True)

    @loop_fuse(threshold=2, on_loop_detected=callback)
    def my_func(action):
        return action

    my_func("test")

    with pytest.raises(LoopDetectedError):
        my_func("test")

    assert len(callback_called) == 1
