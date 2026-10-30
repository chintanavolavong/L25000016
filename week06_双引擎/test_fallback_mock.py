from unittest.mock import Mock
from llm import LLM

llm = LLM()

# 模拟本地引擎失败
llm.local.ask = Mock(
    side_effect=ConnectionError("模拟本地服务不可用")
)

# 模拟云端引擎正常返回，不产生真实API费用
llm.api.ask = Mock(
    return_value="模拟云端回答成功"
)

print("测试：本地失败，自动切换云端")
print("测试类型：模拟测试")

try:
    result = llm.ask(
        "请简单介绍人工智能。",
        prefer="local"
    )

    print("回答：", result)
    print("本地调用次数：", llm.local.ask.call_count)
    print("云端调用次数：", llm.api.ask.call_count)

    assert llm.local.ask.call_count == 3
    assert llm.api.ask.call_count == 1

    print("测试结果：通过")

except Exception as e:
    print("测试结果：失败")
    print("错误原因：", str(e))