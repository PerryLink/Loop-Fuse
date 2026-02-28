import hashlib
from typing import Any

def generate_fingerprint(action: Any) -> str:
    """生成操作指纹（MD5 哈希）"""
    action_str = str(action)
    return hashlib.md5(action_str.encode('utf-8')).hexdigest()
