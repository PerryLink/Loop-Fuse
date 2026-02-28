from loop_fuse import loop_fuse

def my_callback(history, fingerprint, cost_saved):
    """自定义熔断回调"""
    print(f"\n[回调] 检测到循环！")
    print(f"[回调] 节省成本: ${cost_saved:.4f}")

@loop_fuse(threshold=3, on_loop_detected=my_callback)
def agent_loop(action):
    print(f"执行: {action}")

if __name__ == "__main__":
    try:
        for i in range(5):
            agent_loop("重复操作")
    except Exception as e:
        print(f"\n捕获异常: {e}")
