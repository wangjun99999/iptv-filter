import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"
OUTPUT_FILE = "output.m3u"

TARGET_GROUPS = [
    "上海电信-组播1",
    "上海电信-组播2",
    "上海电信-组播3",
    "北京联通-组播1",
    "北京联通-组播2",
    "北京联通-组播3",
    "山东联通-组播1",
    "山东联通-组播2",
    "山东联通-组播3",
    "山东电信-组播1",
    "山东电信-组播2",
    "山东电信-组播3",
]

def fetch_m3u():
    r = requests.get(SOURCE_URL, timeout=20)
    r.raise_for_status()
    return r.text.replace("\ufeff", "").splitlines()

lines = fetch_m3u()

result = ["#EXTM3U"]

i = 0
current_keep = False

while i < len(lines):
    line = lines[i].strip()

    # 判断是不是“分组标题行”
    hit_group = None
    for g in TARGET_GROUPS:
        # 只允许精确命中“组播X”
        if re.search(rf"{re.escape(g)}(,|$)", line):
            hit_group = g
            break

    if hit_group:
        # 进入一个允许的分组
        result.append(f"{hit_group},#genre#")
        current_keep = True
        i += 1
        continue

    # 碰到其他分组标题，直接关闭 keep
    if "组播" in line and line.endswith("#genre#"):
        current_keep = False
        i += 1
        continue

    # 只有在允许的分组里，才保留频道行
    if current_keep:
        if line:
            result.append(line)

    i += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
