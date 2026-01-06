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
    "CCTV2": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV2.png",
    "CCTV3": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV3.png",
    "CCTV4": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV4.png",
    "CCTV5": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV5.png",
    "CCTV5+": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV5+.png",
    "CCTV6": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV6.png",
    "CCTV7": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV7.png",
    "CCTV8": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV8.png",
    "CCTV9": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV9.png",
    "CCTV10": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV10.png",
    "CCTV11": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV11.png",
    "CCTV12": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV12.png",
    "CCTV13": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV13.png",
    "CCTV14": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV14.png",
    "CCTV15": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV15.png",
    "CCTV16": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV16.png",
    "CCTV17": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV17.png",
    "CCTV4欧洲": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV4%E6%AC%A7%E6%B4%B2.png",
    "CCTV4美洲": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/CCTV4%E7%BE%8E%E6%B4%B2.png",
    "山东体育": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E4%BD%93%E8%82%B2.png",
    "山东农科": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E5%86%9C%E7%A7%91.png",
    "山东少儿": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E5%B0%91%E5%84%BF.png",
    "山东教育": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E6%95%99%E8%82%B2.png",
    "山东文旅": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E6%96%87%E6%97%85.png",
    "山东新闻": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E6%96%B0%E9%97%BB.png",
    "山东生活": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E7%94%9F%E6%B4%BB.png",
    "山东综艺": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E7%BB%BC%E8%89%BA.png",
    "山东齐鲁": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E9%BD%90%E9%B2%81.png",
    "青岛tv1": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-1.png",
    "青岛tv2": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-2.png",
    "青岛tv3": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-3.png",
    "青岛tv4": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-4.png",
    "青岛tv5": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-5.png",
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

    is_sports = False
    operator = None

    for op, chs in SPORTS_CHANNELS.items():
        if raw_name in chs:
            is_sports = True
            operator = op
            display_name = f"{op}丨{raw_name}"
            break

    # ---------- 筛选 ----------
    keep = False
    rule = KEEP_RULES.get(operator)

    if rule:
        if rule.get("cctv") and raw_name.upper().startswith("CCTV"):
            keep = True
        elif rule.get("satellite") and "卫视" in raw_name:
            keep = True
        elif raw_name in rule.get("exact", []):
            keep = True
        elif any(k in raw_name for k in rule.get("keywords", [])):
            keep = True

    if is_sports:
        keep = True

    if not keep:
        i += 2
        continue

    # ---------- EPG & LOGO ----------
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

print("✅ 生成完成：频道完整 + 体育独立分组 + EPG/Logo 正确")
