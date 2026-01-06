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

# --------------------- 主频道筛选规则 ---------------------
KEEP_RULES = {
    "山东电信": {
        "cctv": True,
        "satellite": True,
        "keywords": [
            "山东",
            "青岛1","青岛2","青岛3","青岛4","青岛5","青岛6",
            "青岛QTV1","青岛QTV2","青岛QTV3","青岛QTV4"
        ]
    },
    "上海电信": {
        "cctv": True,
        "satellite": True,
        "exact": [
            "东方影视",
            "新闻综合",
            "都市频道",
            "都市剧场",
            "欢笑剧场",
            "五星体育"
        ]
    },
    "山东联通": {
        "cctv": True,
        "satellite": True,
        "keywords": [
            "山东",
            "青岛QTV1","青岛QTV2","青岛QTV3","青岛QTV4"
        ]
    },
    "北京联通": {
        "cctv": True,
        "satellite": True,
        "keywords": [
            "北京",
            "青岛QTV1","青岛QTV2","青岛QTV3","青岛QTV4"
        ]
    }
}

# tvg-logo 映射（示例）
LOGO_MAP = {
    "CCTV1": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV1.png",
    "CCTV2": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV2.png",
    "CCTV3": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV3.png",
    "CCTV4": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV4.png",
    "CCTV5": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV5.png",
    "CCTV5+": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV5+.png",
    "CCTV6": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV6.png",
    "山东体育": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E4%BD%93%E8%82%B2.png",
    "青岛tv1": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-1.png",
    "青岛tv2": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-2.png",
    "青岛tv3": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-3.png",
    "五星体育": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV5.png",
}

# --------------------- 工具函数 ---------------------
def guess_tvg_id(name):
    if name in LOCAL_TVG:
        return LOCAL_TVG[name]
    if re.match(r"CCTV[- ]?\d+", name.upper()):
        return name.upper().replace(" ", "")
    return name.replace(" ", "")

def guess_logo(tvg_id):
    return LOGO_MAP.get(tvg_id, f"https://example.com/logo/{tvg_id}.png")

# --------------------- 读取源 ---------------------
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

    # 判断体育频道
    is_sports = False
    operator_sports = None
    for operator, channels in SPORTS_CHANNELS.items():
        if raw_name in channels:
            raw_name_display = f"{operator}丨{raw_name}"
            is_sports = True
            operator_sports = operator
            break

    # 判断主频道是否保留
    keep = False
    operator_keep = None
    for op, rule in KEEP_RULES.items():
        # 精确匹配
        if "exact" in rule and raw_name in rule["exact"]:
            keep = True
            operator_keep = op
            break
        # 关键字匹配
        if "keywords" in rule:
            for kw in rule["keywords"]:
                if kw in raw_name:
                    keep = True
                    operator_keep = op
                    break
        # CCTV
        if rule.get("cctv") and raw_name.upper().startswith("CCTV"):
            keep = True
            operator_keep = op
            break
        # 卫视
        if rule.get("satellite") and "卫视" in raw_name:
            keep = True
            operator_keep = op
            break
        if keep:
            break

    if not keep and not is_sports:
        i += 2
        continue

    tvg_id = guess_tvg_id(raw_name)
    tvg_name = raw_name if not is_sports else raw_name
    tvg_logo = guess_logo(tvg_id)

    # 修改 EXTINF
    if is_sports:
        extinf_new = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{raw_name}" tvg-logo="{tvg_logo}" group-title="体育频道",{raw_name_display}'
    else:
        # 尽量保留原group-title
        m = re.search(r'group-title="([^"]+)"', extinf)
        group = m.group(1) if m else "其他频道"
        extinf_new = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{raw_name}" tvg-logo="{tvg_logo}" group-title="{group}",{raw_name}'

    out.append(extinf_new)
    out.append(url)
    i += 2

# --------------------- 输出 ---------------------
with open("output_epg.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("生成完成：output_epg.m3u (含体育频道 + 主频道 + Logo + group-title)")
