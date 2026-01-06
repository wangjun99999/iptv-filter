import requests
import re

# --------------------- 配置 ---------------------

SRC_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"

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

# --------------------- 工具函数 ---------------------

def guess_tvg_id(name):
    name_upper = name.upper()
    m = re.match(r"CCTV[- ]?(\d+)", name_upper)
    if m:
        return f"CCTV{m.group(1)}"
    if name_upper == "CCTV5+":
        return "CCTV5+"
    if name in LOCAL_TVG:
        return LOCAL_TVG[name]
    if "卫视" in name:
        return name.replace("卫视", "") + "卫视"
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
    if not lines[i].startswith("#EXTINF"):
        i += 1
        continue

    extinf = lines[i]
    url = lines[i + 1]
    name = extinf.split(",")[-1].strip()

    is_sports = False
    for operator, channels in SPORTS_CHANNELS.items():
        if name in channels:
            name = f"{operator}丨{name}"
            is_sports = True
            break

    tvg_id = guess_tvg_id(name)
    tvg_logo = guess_logo(tvg_id)

    # 只插入属性，不整体替换
    if 'tvg-id=' not in extinf:
        extinf = extinf.replace(
            "#EXTINF:-1",
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" tvg-logo="{tvg_logo}"'
        )

# ---------- 是否保留该频道 ----------
keep = False

# 判断运营商
operator = None
for op in KEEP_RULES:
    if op in name:
        operator = op
        break

if operator:
    rule = KEEP_RULES[operator]

    # CCTV
    if rule.get("cctv") and name.upper().startswith("CCTV"):
        keep = True

    # 卫视
    elif rule.get("satellite") and "卫视" in name:
        keep = True

    # 精确匹配
    elif "exact" in rule and name in rule["exact"]:
        keep = True

    # 关键字匹配
    elif "keywords" in rule:
        for kw in rule["keywords"]:
            if kw in name:
                keep = True
                break

# 体育频道是“额外允许”
if not keep:
    for channels in SPORTS_CHANNELS.values():
        if name in channels:
            keep = True
            break

# 不保留就跳过
if not keep:
    i += 2
    continue
    
    # 体育频道统一分组
    if is_sports:
        if 'group-title=' in extinf:
            extinf = re.sub(r'group-title="[^"]*"', 'group-title="体育频道"', extinf)
        else:
            extinf = extinf.replace(
                "#EXTINF:-1",
                '#EXTINF:-1 group-title="体育频道"'
            )

    out.append(extinf)
    out.append(url)
    i += 2

# --------------------- 输出 ---------------------

with open("output_epg.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("生成完成：保留原 group-title，体育频道独立分组，全部含 EPG + Logo")
