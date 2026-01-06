import requests
import re

SRC_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"

# ---------- 本地频道映射 ----------
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
    "青岛QTV4": "青岛tv4",
}

# ---------- 体育频道 ----------
SPORTS_CHANNELS = {
    "广东联通": ["广东体育频道"],
    "山东联通": ["山东体育休闲", "青岛QTV3"],
    "北京联通": ["北京体育休闲"],
}

# ---------- 主筛选规则 ----------
KEEP_RULES = {
    "山东电信": {
        "cctv": True,
        "satellite": True,
        "keywords": ["山东", "青岛"]
    },
    "上海电信": {
        "cctv": True,
        "satellite": True,
        "exact": ["东方影视", "新闻综合", "都市频道", "五星体育"]
    },
    "山东联通": {
        "cctv": True,
        "satellite": True,
        "keywords": ["山东", "青岛"]
    },
    "北京联通": {
        "cctv": True,
        "satellite": True,
        "keywords": ["北京"]
    }
}

# ---------- LOGO ----------
LOGO_MAP = {
    "CCTV1": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV1.png",
    "CCTV5": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV5.png",
    "CCTV5+": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV5+.png",
    "山东体育": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/山东体育.png",
    "青岛tv3": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-3.png",
}

# ---------- 工具函数 ----------
def guess_tvg_id(name):
    n = name.upper()
    m = re.match(r"CCTV[- ]?(\d+)", n)
    if m:
        return f"CCTV{m.group(1)}"
    if name in LOCAL_TVG:
        return LOCAL_TVG[name]
    if "卫视" in name:
        return name.replace("卫视", "") + "卫视"
    return name.replace(" ", "")

def guess_logo(tvg_id):
    return LOGO_MAP.get(tvg_id, f"https://example.com/logo/{tvg_id}.png")

# ---------- 主处理 ----------
resp = requests.get(SRC_URL)
resp.encoding = "utf-8"
lines = resp.text.splitlines()

out = ["#EXTM3U"]
i = 0

while i < len(lines):
    if not lines[i].startswith("#EXTINF"):
        i += 1
        continue

    extinf = lines[i]
    url = lines[i + 1]

    raw_name = extinf.split(",")[-1].strip()
    display_name = raw_name

    # ---------- 判断是否体育频道 ----------
    is_sports = False
    operator = None
    for op, chs in SPORTS_CHANNELS.items():
        if raw_name in chs:
            is_sports = True
            operator = op
            display_name = f"{op}丨{raw_name}"
            break

    # ---------- 筛选逻辑 ----------
    keep = False
    rule = None
    # 判断规则是否匹配
    for op, r in KEEP_RULES.items():
        if op in display_name:
            rule = r
            break
    if rule:
        if rule.get("cctv") and raw_name.upper().startswith("CCTV"):
            keep = True
        elif rule.get("satellite") and "卫视" in raw_name:
            keep = True
        elif raw_name in rule.get("exact", []):
            keep = True
        elif any(k in raw_name for k in rule.get("keywords", [])):
            keep = True
    # 体育频道强制保留
    if is_sports:
        keep = True

    # 保留所有其他未在规则里的频道（保证非体育频道也输出）
    if not rule and not is_sports:
        keep = True

    if not keep:
        i += 2
        continue

    # ---------- EPG + LOGO ----------
    tvg_id = guess_tvg_id(raw_name)
    logo = guess_logo(tvg_id)
    if "tvg-id=" not in extinf:
        extinf = extinf.replace(
            "#EXTINF:-1",
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{raw_name}" tvg-logo="{logo}"'
        )

    # ---------- 体育分组 ----------
    if is_sports:
        if "group-title=" in extinf:
            extinf = re.sub(r'group-title="[^"]*"', 'group-title="体育频道"', extinf)
        else:
            extinf = extinf.replace(
                "#EXTINF:-1",
                '#EXTINF:-1 group-title="体育频道"'
            )

    out.append(f"{extinf},{display_name}")
    out.append(url)
    i += 2

with open("output_epg.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("✅ 完成：体育 + 非体育频道均保留，EPG + LOGO + group-title 正确")
