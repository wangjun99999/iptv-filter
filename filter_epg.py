import re

INPUT = "output_epg.m3u"
OUTPUT = "output_epg.m3u"

# 上海电信专用白名单
SHANGHAI_WHITELIST = {
    "东方影视",
    "新闻综合",
    "都市频道",
    "都市剧场",
    "欢笑剧场",
    "五星体育",
}

def is_cctv(name):
    return name.upper().startswith("CCTV")

def is_satellite(name):
    return "卫视" in name

def is_shandong(name):
    return "山东" in name

def is_beijing(name):
    return "北京" in name

def is_qingdao_1_6(name):
    return bool(re.search(r"(青岛|QTV)[1-6]", name, re.I))

def is_qingdao_1_4(name):
    return bool(re.search(r"(青岛|QTV)[1-4]", name, re.I))

def shanghai_special(name):
    return any(x in name for x in SHANGHAI_WHITELIST)

def allow_channel(group, name):
    # 公共
    if is_cctv(name) or is_satellite(name):
        return True

    # 山东电信
    if "山东电信" in group:
        return is_shandong(name) or is_qingdao_1_6(name)

    # 上海电信
    if "上海电信" in group:
        return shanghai_special(name)

    # 山东联通
    if "山东联通" in group:
        return is_shandong(name) or is_qingdao_1_4(name)

    # 北京联通
    if "北京联通" in group:
        return is_beijing(name) or is_qingdao_1_4(name)

    return False


out = ["#EXTM3U"]

with open(INPUT, encoding="utf-8") as f:
    lines = f.read().splitlines()

i = 0
while i < len(lines):
    if lines[i].startswith("#EXTINF"):
        extinf = lines[i]
        url = lines[i + 1]

        # 频道名
        name = extinf.split(",")[-1].strip()
        # 组名
        m = re.search(r'group-title="([^"]+)"', extinf)
        group = m.group(1) if m else ""

        if allow_channel(group, name):
            out.append(extinf)
            out.append(url)

        i += 2
    else:
        i += 1

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("筛选完成：output_epg.m3u")
