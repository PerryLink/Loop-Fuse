from loop_fuse import loop_fuse

@loop_fuse(threshold=3, cost_per_call=0.01)
def expensive_agent_call(query):
    """模拟昂贵的 API 调用"""
    print(f"调用 API: {query}")
    return f"结果: {query}"

if __name__ == "__main__":
    try:
        for i in range(10):
            expensive_agent_call("相同的查询")
    except Exception as e:
        print(f"\n捕获异常: {e}")
