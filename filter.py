import requests

SOURCE_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"
OUTPUT_FILE = "output.m3u"

ALLOW_KEYS = [
    "上海电信",
    "北京联通",
    "山东联通",
    "山东电信",
]

def fetch_m3u():
    r = requests.get(SOURCE_URL, timeout=20)
    r.raise_for_status()
    # 处理 BOM / 奇怪编码
    return r.text.replace("\ufeff", "").splitlines()

lines = fetch_m3u()

result = ["#EXTM3U"]

i = 0
while i < len(lines):
    line = lines[i].strip()

    for key in ALLOW_KEYS:
        for n in (1, 2, 3):
            name = f"{key}-组播{n}"

            # 命中分组标题（不管什么写法）
            if name in line:
                result.append(f"{name},#genre#")
                i += 1

                # 收集该分组下的频道
                while i < len(lines):
                    l = lines[i].strip()

                    # 碰到下一个分组就停
                    if any(k in l and "组播" in l for k in ALLOW_KEYS):
                        i -= 1
                        break

                    if l:
                        result.append(l)

                    i += 1
                break
    i += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
