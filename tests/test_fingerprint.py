from loop_fuse.fingerprint import generate_fingerprint

def test_same_string_same_fingerprint():
    """相同字符串生成相同指纹"""
    fp1 = generate_fingerprint("test")
    fp2 = generate_fingerprint("test")
    assert fp1 == fp2

def test_different_string_different_fingerprint():
    """不同字符串生成不同指纹"""
    fp1 = generate_fingerprint("test1")
    fp2 = generate_fingerprint("test2")
    assert fp1 != fp2

def test_dict_fingerprint():
    """字典也能生成指纹"""
    fp = generate_fingerprint({"action": "search", "query": "test"})
    assert isinstance(fp, str)
    assert len(fp) == 32  # MD5 长度
