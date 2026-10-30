# W4 命令行学科问答机器人（API 版）
# 依赖：pip install openai python-dotenv
# 运行：python week4_api_bot.py "把字句的教学难点有哪些"
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  加载 .env

weekpath.load_env()

import openai  # noqa: E402

BASE_URL = "https://api.deepseek.com/v1"  # 通义：https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL = "deepseek-chat"  # 通义：qwen-plus

_client = None


def get_client():
    """按需创建客户端，避免在导入模块时因缺少密钥而报错。"""
    global _client
    if _client is None:
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("未设置 DEEPSEEK_API_KEY。请在本地 .env 文件中配置密钥。")
        _client = openai.OpenAI(base_url=BASE_URL, api_key=key)
    return _client


def ask(question, temperature=0.7, max_tokens=800):
    r = get_client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return r.choices[0].message.content


if __name__ == "__main__":
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("错误：未设置 DEEPSEEK_API_KEY。")
        print("处理方法：在本地 .env 文件中填写密钥，且不要将该文件上传至 GitHub。")
        sys.exit(1)

    q = " ".join(sys.argv[1:]) or "把字句的教学难点有哪些"
    try:
        ans = ask(q)
    except openai.APITimeoutError:
        print("错误：请求超时，请检查网络或调大 timeout。")
        sys.exit(1)
    except openai.APIError as exc:
        print("错误：API 请求失败：%s" % exc)
        sys.exit(1)
    print(ans)

    # 日志固定写入代码包根目录；请确保 .gitignore 排除该文件。
    with open(weekpath.root_path("chat_log.txt"), "a", encoding="utf-8") as f:
        f.write("Q: %s\nA: %s\n\n" % (q, ans))
