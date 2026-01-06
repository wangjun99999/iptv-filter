import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"
OUTPUT_FILE = "output.m3u"

TARGET_GROUPS = {
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
}

def fetch_m3u():
    r = requests.get(SOURCE_URL, timeout=20)
    r.raise_for_status()
    return r.text.replace("\ufeff", "").splitlines()

lines = fetch_m3u()

out = ["#EXTM3U"]
i = 0

while i < len(lines):
    line = lines[i].strip()

    # 只处理 EXTINF 行
    if line.startswith("#EXTINF"):
        m = re.search(r'group-title="([^"]+)"', line)
        if m and m.group(1) in TARGET_GROUPS:
            # 保留 EXTINF
            out.append(line)

            # 紧跟的一行一定是播放地址
            if i + 1 < len(lines):
                out.append(lines[i + 1].strip())
            i += 2
            continue

        # 不在目标组，直接跳过 EXTINF + URL
        i += 2
        continue

    i += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
