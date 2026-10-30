import time
from llm import LLM

llm = LLM()

tests = [
    ("测试1：本地正常", "你好，请用一句话介绍人工智能。", "local"),
    ("测试2：云端优先", "什么是人工智能？", "api"),
    ("测试3：本地中文回答", "请介绍中国文化。", "local"),
    ("测试4：云端中文回答", "请解释机器学习。", "api"),
    ("测试5：本地学科问题", "什么是HSK4？", "local"),
]

for name, prompt, prefer in tests:
    print("\n" + "=" * 40)
    print(name)
    print("首选引擎:", prefer)

    start = time.time()

    try:
        answer = llm.ask(prompt, prefer=prefer)
        print("回答:", answer)
        print("结果: 成功")
    except Exception as e:
        print("结果: 失败")
        print("错误:", str(e))

    print("耗时:", round(time.time() - start, 2), "秒")