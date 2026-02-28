from loop_fuse import loop_fuse

@loop_fuse(window_size=5, threshold=3)
def agent_loop(action):
    """模拟 Agent 循环"""
    print(f"执行操作: {action}")
    return f"完成: {action}"

if __name__ == "__main__":
    actions = ["搜索天气", "搜索新闻", "搜索新闻", "搜索新闻"]

    try:
        for action in actions:
            agent_loop(action)
    except Exception as e:
        print(f"\n捕获异常: {e}")
