# W3 生词表 CSV -> 自动生成练习题
# 运行: python vocab_tool.py
import os
import csv
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402 统一解析 data/ 路径，换目录也不会找不到文件

DATA = weekpath.data_path("生词表.csv")

# ========== 写法A：手写骨架版 ==========
def load_words(path=DATA):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def filter_by_level(words, level="4"):
    return [w for w in words if str(w["HSK等级"]) == str(level)]

def count_by_pos(words):
    d = {}
    for w in words:
        d[w["词性"]] = d.get(w["词性"], 0) + 1
    return d

def gen_exercises(words, out=None):
    out = out or weekpath.root_path("练习.txt")
    with open(out, "w", encoding="utf-8") as f:
        for w in words:
            f.write(f"用【{w['词汇']}】造一个句子。\n")

if __name__ == "__main__":
    # --- 手写版运行 ---
    words = load_words()
    hsk4_words = filter_by_level(words)
    gen_exercises(hsk4_words)
    print("【手写版完成】HSK4 词汇数量:", len(hsk4_words))

    # --- 写法B：AI辅助修改版 ---
    print("\n--- AI辅助优化版 ---")
    # 提示词：读取生词表，筛选HSK4，统计词性，生成练习，保存到练习.txt
    
    # 1. 读取文件（保持原路径写法，兼容weekpath）
    words_ai = load_words()
    
    # 2. 筛选HSK4词汇
    hsk4_ai = [w for w in words_ai if str(w["HSK等级"]) == "4"]
    
    # 3. 统计词性分布
    pos_count = count_by_pos(hsk4_ai)
    print("词性统计:", pos_count)
    
    # 4. 生成练习写入文件
    gen_exercises(hsk4_ai)
    print("【AI版完成】HSK4 词汇数量:", len(hsk4_ai))

    # --- 修改差异说明 ---
    print("\n" + "="*40)
    print("📝 修改差异记录：")
    print("1. 保留原路径写法 weekpath：适配课程统一目录结构，避免找不到文件")
    print("2. 不删除原函数：load_words/filter_by_level 复用手写逻辑，结构清晰易读")
    print("3. 增加词性统计 count_by_pos：补充数据维度，符合练习要求")
    print("4. 统一输出文件 练习.txt：严格按老师要求命名，不随意改名")
    print("5. 保留if __name__ == '__main__'：区分函数定义与执行入口，规范代码结构")