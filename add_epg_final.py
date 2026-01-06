import requests
import re

# --------------------- 配置 ---------------------

SRC_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"

# 地方台 tvg-id 映射
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
    "青岛1": "青岛tv1",
    "青岛2": "青岛tv2",
    "青岛3": "青岛tv3",
    "青岛4": "青岛tv4",
    "青岛5": "青岛tv5",
    "青岛6": "青岛tv6",
    "青岛QTV1": "青岛tv1",
    "青岛QTV2": "青岛tv2",
    "青岛QTV3": "青岛tv3",
    "青岛QTV4": "青岛tv4",
    "新闻综合": "上海新闻综合",
    "都市频道": "上海都市",
    "东方影视": "上视东方影视",
    "北京新闻频道": "BTV新闻",
    "北京体育休闲": "BTV体育",
}

# 体育频道
SPORTS_CHANNELS = {
    "广东联通": ["广东体育频道"],
    "山东联通": ["山东体育休闲", "青岛QTV3"],
    "重庆联通": ["重庆文体娱乐"],
    "辽宁联通": ["辽宁体育休闲"],
    "北京联通": ["北京体育休闲"],
    "天津联通": ["天津体育频道"],
    "广东电信": ["广东体育频道", "深圳体育健康"],
    "山东电信": ["山东体育频道", "青岛3"],
    "吉林电信": ["吉林篮球"],
    "重庆电信": ["重庆文体娱乐"],
    "福建电信": ["福建文体频道"],
    "北京电信": ["北京体育休闲"],
    "湖北电信": ["武汉文体频道"],
    "陕西电信": ["陕西体育休闲"],
    "天津电信": ["天津体育频道"],
    "江苏电信": ["江苏体育休闲"],
    "上海电信": ["五星体育"],
    "四川电信": ["成都公共频道"],
    "云南电信": ["云南康旅频道"],
    "浙江电信": ["杭州青少"],
}

# 主频道 group-title 白名单
KEEP_GROUPS = ["山东电信", "山东联通", "上海电信", "北京联通"]

# tvg-logo 映射示例
LOGO_MAP = {
    "山东体育": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E4%BD%93%E8%82%B2.png",
    "青岛tv3": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-3.png",
    "五星体育": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV5.png",
}

# --------------------- 工具函数 ---------------------

def guess_tvg_id(name):
    if name in LOCAL_TVG:
        return LOCAL_TVG[name]
    return name.replace(" ", "")

def guess_logo(tvg_id):
    return LOGO_MAP.get(tvg_id, f"https://example.com/logo/{tvg_id}.png")

# --------------------- 主处理 ---------------------

resp = requests.get(SRC_URL)
resp.encoding = "utf-8"
lines = resp.text.splitlines()

out = ["#EXTM3U"]
i = 0

while i < len(lines):
    line = lines[i]
    if not line.startswith("#EXTINF"):
        i += 1
        continue

    extinf = lines[i]
    url = lines[i + 1]
    raw_name = extinf.split(",")[-1].strip()

    # group-title
    m = re.search(r'group-title="([^"]+)"', extinf)
    group = m.group(1) if m else "其他频道"

    # 体育频道
    is_sports = False
    sports_name = ""
    for operator, channels in SPORTS_CHANNELS.items():
        if raw_name in channels:
            is_sports = True
            sports_name = f"{operator}丨{raw_name}"
            break

    # 判断是否保留
    if group not in KEEP_GROUPS and not is_sports:
        i += 2
        continue

    tvg_id = guess_tvg_id(raw_name)
    tvg_name = raw_name
    tvg_logo = guess_logo(tvg_id)

    if is_sports:
        extinf_new = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" group-title="体育频道",{sports_name}'
    else:
        extinf_new = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" group-title="{group}",{raw_name}'

    out.append(extinf_new)
    out.append(url)
    i += 2

# --------------------- 输出 ---------------------

with open("output_epg.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("生成完成：output_epg.m3u（只保留指定 group + 体育频道，含 tvg + logo）")
