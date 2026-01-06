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
    r = requests.get(SOURCE_URL, timeout=15)
    r.raise_for_status()
    return r.text.splitlines()

lines = fetch_m3u()

groups = {}
current_group = None
buffer = []

for line in lines:
    if line.endswith(",#genre#"):
        if current_group:
            groups[current_group] = buffer
        current_group = line.strip()
        buffer = []
    else:
        if current_group:
            buffer.append(line)

if current_group:
    groups[current_group] = buffer

result = ["#EXTM3U"]

for key in ALLOW_KEYS:
    for i in (1, 2, 3):
        g = f"{key}-组播{i},#genre#"
        if g in groups:
            result.append(g)
            result.extend(groups[g])

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
