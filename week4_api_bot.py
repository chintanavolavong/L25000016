# W4 å‘½ä»¤è¡Œå­¦ç§‘é—®ç­”æœºå™¨äººï¼ˆAPI ç‰ˆï¼‰
# ä¾èµ–ï¼špip install openai python-dotenv
# è¿è¡Œï¼špython week4_api_bot.py "æŠŠå­—å¥çš„æ•™å­¦éš¾ç‚¹æœ‰å“ªäº›"
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  åŠ è½½ .env

weekpath.load_env()

import openai  # noqa: E402

BASE_URL = "https://api.deepseek.com/v1"          # é€šä¹‰ï¼šhttps://dashscope.aliyuncs.com/compatible-mode/v1
MODEL = "deepseek-chat"                            # é€šä¹‰ï¼šqwen-plus

_client = None


def get_client():
    """æŒ‰éœ€åˆ›å»ºå®¢æˆ·ç«¯ï¼šè¿™æ ·"æ²¡é…å¯†é’¥"èƒ½åœ¨ __main__ é‡Œè¢«å‹å¥½æç¤ºï¼Œ
    è€Œä¸æ˜¯åœ¨ import é˜¶æ®µå°±æŠ›å‡ºçœ‹ä¸æ‡‚çš„ OpenAIErrorã€‚"""
    global _client
    if _client is None:
        key = os.getenv("DEEPSEEK_API_KEY")
if not key:
    raise RuntimeError("è¯·å…ˆè®¾ç½® DEEPSEEK_API_KEY çŽ¯å¢ƒå˜é‡")


        _client = openai.OpenAI(base_url=BASE_URL, api_key=key)  # å¯†é’¥å¿…é¡»æ¥è‡ªçŽ¯å¢ƒå˜é‡
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
    #if not os.getenv("DEEPSEEK_API_KEY"):
       # print("é”™è¯¯ï¼šæœªè®¾ç½® DEEPSEEK_API_KEYã€‚")
       # print("  å¤„ç†ï¼šå¤åˆ¶ .env.example ä¸º .env å¹¶å¡«å…¥å¯†é’¥ï¼Œé‡å¯ç»ˆç«¯åŽé‡è¯•ã€‚")
       # sys.exit(1)
    q = " ".join(sys.argv[1:]) or "æŠŠå­—å¥çš„æ•™å­¦éš¾ç‚¹æœ‰å“ªäº›"
    try:
        ans = ask(q)
    except openai.APITimeoutError:
        print("é”™è¯¯ï¼šè¯·æ±‚è¶…æ—¶ï¼Œè¯·æ£€æŸ¥ç½‘ç»œæˆ–è°ƒå¤§ timeoutã€‚")
        sys.exit(1)
    print(ans)
    # æ—¥å¿—å›ºå®šå†™ä»£ç åŒ…æ ¹ç›®å½•ï¼ˆ.gitignore å·²æŽ’é™¤ï¼‰ï¼Œé¿å…éšæ‰‹å»ºåœ¨å·¥ä½œç›®å½•é‡Œè¢«è¯¯æäº¤
    with open(weekpath.root_path("chat_log.txt"), "a", encoding="utf-8") as f:
        f.write("Q: %s\nA: %s\n\n" % (q, ans))
