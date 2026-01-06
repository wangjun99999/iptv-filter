import requests
import re

# 原始源链接
SRC_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"

# 体育频道映射：运营商 -> [频道名]
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

# 下载原始 m3u
resp = requests.get(SRC_URL)
resp.encoding = 'utf-8'
lines = resp.text.splitlines()

out = []

i = 0
while i < len(lines):
    if lines[i].startswith("#EXTINF"):
        title_line = lines[i]
        url_line = lines[i + 1]

        # 提取频道名和 group-title
        m_group = re.search(r'group-title="([^"]+)"', title_line)
        group_name = m_group.group(1) if m_group else ""
        name = title_line.split(",")[-1].strip()

        # 检查是否在 SPORTS_CHANNELS 中
        for operator, channels in SPORTS_CHANNELS.items():
            if name in channels:
                # 构建新的 EXTINF
                new_name = f"{operator}丨{name}"
                new_line = f'#EXTINF:-1 group-title="体育频道",{new_name}'
                out.append(new_line)
                out.append(url_line)
                break

        i += 2
    else:
        i += 1

# 写入到文件，追加到现有 output_epg.m3u 后
with open("output_epg.m3u", "a", encoding="utf-8") as f:
    f.write("\n" + "\n".join(out))

print("体育频道已添加完成，group-title=\"体育频道\"")
