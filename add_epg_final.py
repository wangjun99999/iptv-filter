import requests
import re
from collections import defaultdict

SRC_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"
OUT_FILE = "output_epg.m3u"

# ======================================================
# tvg-id / tvg-name 映射（EPG 核心）
# ======================================================

LOCAL_TVG = {
    "CCTV-1综合": {"id": "CCTV1", "name": "CCTV1"},
    "CCTV-2财经": {"id": "CCTV2", "name": "CCTV2"},
    "CCTV-3综艺": {"id": "CCTV3", "name": "CCTV3"},
    "CCTV-4中文国际": {"id": "CCTV4", "name": "CCTV4"},
    "CCTV-4 欧洲": {"id": "CCTV4欧洲", "name": "CCTV4欧洲"},
    "CCTV-4欧洲": {"id": "CCTV4欧洲", "name": "CCTV4欧洲"},
    "CCTV-4 北美": {"id": "CCTV4美洲", "name": "CCTV4美洲"},
    "CCTV-4美洲": {"id": "CCTV4美洲", "name": "CCTV4美洲"},
    "CCTV-5体育": {"id": "CCTV5", "name": "CCTV5"},
    "CCTV-5+体育赛事": {"id": "CCTV5+", "name": "CCTV5+"},
    "CCTV5+体育赛事": {"id": "CCTV5+", "name": "CCTV5+"},
    "CCTV-6电影": {"id": "CCTV6", "name": "CCTV6"},
    "CCTV-7国防军事": {"id": "CCTV7", "name": "CCTV7"},
    "CCTV-8电视剧": {"id": "CCTV8", "name": "CCTV8"},
    "CCTV-9纪录": {"id": "CCTV9", "name": "CCTV9"},
    "CCTV-10科教": {"id": "CCTV10", "name": "CCTV10"},
    "CCTV-11戏曲": {"id": "CCTV11", "name": "CCTV11"},
    "CCTV-12社会与法": {"id": "CCTV12", "name": "CCTV12"},
    "CCTV-13新闻": {"id": "CCTV13", "name": "CCTV13"},
    "CCTV-14少儿": {"id": "CCTV14", "name": "CCTV14"},
    "CCTV-15音乐": {"id": "CCTV15", "name": "CCTV15"},
    "CCTV-16奥林匹克": {"id": "CCTV16", "name": "CCTV16"},
    "CCTV-17农业农村": {"id": "CCTV17", "name": "CCTV17"},
    "CCTV4K超高清": {"id": "CCTV4K", "name": "CCTV4K"},
    
    "山东体育频道": {"id": "山东体育休闲", "name": "山东体育休闲"},
    "山东新闻频道": {"id": "山东新闻", "name": "山东新闻"},
    "山东农科频道": {"id": "山东农科", "name": "山东农科"},
    "山东少儿频道": {"id": "山东少儿", "name": "山东少儿"},
    "山东教育频道": {"id": "山东教育", "name": "山东教育"},
    "山东教育卫视": {"id": "山东教育", "name": "山东教育"},
    "山东文旅频道": {"id": "山东文旅", "name": "山东文旅"},
    "山东生活频道": {"id": "山东生活", "name": "山东生活"},
    "山东综艺频道": {"id": "山东综艺", "name": "山东综艺"},
    "山东齐鲁频道": {"id": "山东齐鲁", "name": "山东齐鲁"},
    "青岛QTV1": {"id": "青岛新闻综合", "name": "青岛新闻综合"},
    "青岛QTV2": {"id": "青岛生活服务", "name": "青岛生活服务"},
    "青岛QTV3": {"id": "青岛影视", "name": "青岛影视"},
    "青岛QTV4": {"id": "青岛都市", "name": "青岛都市"},
    "青岛1": {"id": "青岛新闻综合", "name": "青岛新闻综合"},
    "青岛2": {"id": "青岛生活服务", "name": "青岛生活服务"},
    "青岛3": {"id": "青岛影视", "name": "青岛影视"},
    "青岛4": {"id": "青岛都市", "name": "青岛都市"},
    "青岛5": {"id": "青岛教育", "name": "青岛教育"},
    "青岛6": {"id": "青岛tv6", "name": "青岛TV6"},

    "北京卫视4K超高清": {"id": "北京卫视", "name": "北京卫视"},
    "北京影视频道": {"id": "北京影视", "name": "北京影视"},
    "北京文艺频道": {"id": "北京文艺", "name": "北京文艺"},
    "北京新闻频道": {"id": "北京新闻", "name": "北京新闻"},
    "北京生活频道": {"id": "北京生活", "name": "北京生活"},
    "北京财经频道": {"id": "北京财经", "name": "北京财经"},
    "北京卡酷少儿": {"id": "卡酷少儿", "name": "卡酷少儿"},

    "广东体育频道": {"id": "广东体育", "name": "广东体育"},
    "辽宁体育休闲": {"id": "辽宁体育", "name": "辽宁体育"},
    "天津体育频道": {"id": "天津体育", "name": "天津体育"},
    "武汉文体频道": {"id": "武汉文体", "name": "武汉文体"},
    "江苏体育休闲": {"id": "江苏休闲体育", "name": "江苏休闲体育"},
    "成都公共频道": {"id": "成都公共", "name": "成都公共"},
    "云南康旅频道": {"id": "云南康旅", "name": "云南康旅"},
    "福建文体频道": {"id": "福建文体", "name": "福建文体"},
    "杭州青少": {"id": "杭州青少体育", "name": "杭州青少体育"},
    "广东4K超高清": {"id": "广东4K超", "name": "广东4K超"},
}

def guess_tvg(raw_name, display_name):
    info = LOCAL_TVG.get(raw_name)
    if info:
        return info["id"], info["name"]
    return raw_name.replace(" ", ""), display_name

# ======================================================
# 体育频道（顺序即输出顺序）
# ======================================================

SPORTS_CHANNELS = [
    ("广东联通", "广东体育频道"),
    ("广东联通", "CCTV-5体育"),
    ("广东联通", "CCTV-5+体育赛事"),

    ("河北联通", "CCTV-5体育"),
    ("河北联通", "CCTV-5+体育赛事"),

    ("河南联通", "CCTV-5体育"),
    ("河南联通", "CCTV-5+体育赛事"),

    ("重庆联通", "CCTV-5体育"),
    ("重庆联通", "CCTV-5+体育赛事"),
    ("重庆联通", "重庆文体娱乐"),

    ("四川联通", "CCTV-5体育"),
    ("四川联通", "CCTV-5+体育赛事"),

    ("山西联通", "CCTV-5体育"),
    ("山西联通", "CCTV-5+体育赛事"),
    ("山西联通", "CCTV-16奥林匹克"),

    ("海南联通", "CCTV-5体育"),
    ("海南联通", "CCTV-5+体育赛事"),
    ("海南联通", "CCTV-16奥林匹克"),

    ("黑龙江联通", "CCTV-5体育"),
    ("黑龙江联通", "CCTV-5+体育赛事"),

    ("辽宁联通", "CCTV-5体育"),
    ("辽宁联通", "CCTV-5+体育赛事"),
    ("辽宁联通", "CCTV-16奥林匹克"),
    ("辽宁联通", "辽宁体育休闲"),

    ("福建联通", "CCTV-5体育"),
    ("福建联通", "CCTV-5+体育赛事"),
    ("福建联通", "CCTV-16奥林匹克"),

    ("湖北联通", "CCTV-5体育"),
    ("湖北联通", "CCTV5+体育赛事"),     
    ("湖北联通", "CCTV-16奥林匹克"),
    
    ("天津联通", "CCTV-5体育"),
    ("天津联通", "CCTV-5+体育赛事"), 
    ("天津联通", "CCTV-16奥林匹克"),
    ("天津联通", "天津体育频道"),
    
    ("广东电信", "深圳体育健康"),
    ("重庆电信", "重庆文体娱乐"),
    ("福建电信", "福建文体频道"),
    ("湖北电信", "武汉文体频道"),
    ("陕西电信", "陕西体育休闲"),
    ("天津电信", "天津体育频道"),
    ("江苏电信", "江苏体育休闲"),
    ("上海电信", "五星体育"),
    ("四川电信", "成都公共频道"),
    ("云南电信", "云南康旅频道"),
    ("浙江电信", "杭州青少"),
]

# ======================================================
# 地方筛选规则
# ======================================================

KEEP_RULES = {
    "山东电信": {
        "cctv": True,
        "satellite": True,
        "keywords": ["山东", "青岛1", "青岛2", "青岛3", "青岛4", "青岛5", "青岛6"],
    },
    "山东联通": {
        "cctv": True,
        "satellite": True,
        "keywords": ["山东", "青岛QTV1", "青岛QTV2", "青岛QTV3", "青岛QTV4"],
    },
    "北京联通": {
        "cctv": True,
        "satellite": True,
        "keywords": ["北京"],
    },
}

# ======================================================
# 主流程
# ======================================================

resp = requests.get(SRC_URL, timeout=15)
resp.encoding = "utf-8"
lines = resp.text.splitlines()

out = ["#EXTM3U"]
sports_cache = defaultdict(list)

i = 0
while i < len(lines) - 1:
    if not lines[i].startswith("#EXTINF"):
        i += 1
        continue

    extinf = lines[i]
    url = lines[i + 1]
    raw_name = extinf.split(",")[-1].strip()

    m = re.search(r'group-title="([^"]+)"', extinf)
    group = m.group(1) if m else ""

    # ========== 体育 ==========
    for op, ch in SPORTS_CHANNELS:
        if group.startswith(op) and raw_name == ch:
            display = f"{op}丨{raw_name}"
            tvg_id, tvg_name = guess_tvg(raw_name, display)
            sports_cache[(op, ch)].append(
                f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" '
                f'group-title="体育频道",{display}\n{url}'
            )
            break
    else:
        # ========== 地方 ==========
        for prefix, rule in KEEP_RULES.items():
            if group.startswith(prefix):
                keep = (
                    (rule["cctv"] and raw_name.startswith("CCTV"))
                    or (rule["satellite"] and "卫视" in raw_name)
                    or any(k in raw_name for k in rule["keywords"])
                )
                if keep:
                    tvg_id, tvg_name = guess_tvg(raw_name, raw_name)
                    out.append(
                        f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" '
                        f'group-title="{group}",{raw_name}'
                    )
                    out.append(url)
                break

    i += 2

# ========== 输出体育（按顺序） ==========
for key in SPORTS_CHANNELS:
    out.extend(sports_cache.get(key, []))

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print(f"生成完成：{OUT_FILE}")
