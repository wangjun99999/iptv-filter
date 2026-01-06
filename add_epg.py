import re

INPUT = "output.m3u"
OUTPUT = "output_epg.m3u"

# --------- 自定义地方台映射 ---------
# 左边是 output.m3u 的频道名
# 右边是你希望的 tvg-id / tvg-name
LOCAL_TVG = {
    "山东体育频道": "山东体育",
    "山东农科频道": "山东农科",
    "山东少儿频道": "山东少儿",
    "山东教育频道": "山东教育",
    "山东文旅频道": "山东文旅",
    "山东新闻频道": "山东新闻",
    "山东生活频道": "山东生活",
    "山东综艺频道": "山东综艺",
    "山东齐鲁频道": "山东齐鲁",
    "CCTV-5+体育赛事": "CCTV5+",
    "青岛1": "青岛tv1",
    "青岛2": "青岛tv2",
    "青岛3": "青岛tv3",
    "青岛4": "青岛tv4",
    "青岛5": "青岛tv5",
    "青岛6": "青岛tv6",
    "青岛QTV1": "青岛tv1",
    "青岛QTV2": "青岛tv2",
    "青岛QTV3": "青岛tv3",
    "CCTV-4 欧洲": "CCTV4欧洲",
    "CCTV-4欧洲": "CCTV4欧洲",
    "CCTV-4 北美": "CCTV4美洲",
    "CCTV-4美洲": "CCTV4美洲",
    "新闻综合": "上海新闻综合",
    "都市频道": "上海都市",
    "东方影视": "上视东方影视",
    "北京新闻频道": "BTV新闻",
    "北京体育休闲": "BTV体育",
    "北京影视频道": "BTV影视",
    "北京文艺频道": "BTV文艺",
    "北京生活频道": "BTV生活",
    "北京纪实科教": "BTV科教",
    "北京财经频道": "BTV财经",
    # 根据需要继续补充
}

# --------- 央视/卫视映射规则 ---------
def guess_tvg_id(name):
    name = name.strip().upper()
    # CCTV 系列
    m = re.match(r"CCTV[- ]?(\d+)", name)
    if m:
        return f"CCTV{m.group(1)}"
    if name == "CCTV5+":
        return "CCTV5+"
    # 地方台自定义映射
    if name in LOCAL_TVG:
        return LOCAL_TVG[name]
    # 其它卫视 fallback
    if "卫视" in name:
        return name.replace("卫视", "") + "卫视"
    # 默认 fallback
    return name.replace(" ", "")

# --------- 生成带 tvg-id 的 m3u ---------
out = ["#EXTM3U"]

with open(INPUT, encoding="utf-8") as f:
    lines = f.read().splitlines()

i = 0
while i < len(lines):
    if lines[i].startswith("#EXTINF"):
        title_line = lines[i]
        url_line = lines[i + 1]
        # 频道名（逗号后的显示名）
        name = title_line.split(",")[-1].strip()
        tvg_id = guess_tvg_id(name)
        # 替换 EXTINF
        title_line = title_line.replace(
            "#EXTINF:-1",
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}"'
        )
        out.append(title_line)
        out.append(url_line)
        i += 2
    else:
        i += 1

# 写入最终 output_epg.m3u
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("生成完成：output_epg.m3u（央视/卫视 + 自定义地方台映射已加）")
