import re

INPUT = "output.m3u"
OUTPUT = "output_epg.m3u"

def guess_tvg_id(name):
    name = name.upper()

    # CCTV 系列
    m = re.match(r"CCTV[- ]?(\d+)", name)
    if m:
        return f"CCTV{m.group(1)}"

    if name == "CCTV5+":
        return "CCTV5+"

    # 卫视
    if "卫视" in name:
        return name.replace("卫视", "") + "卫视"

    # 其它（按名字原样）
    return name.replace(" ", "")

out = ["#EXTM3U"]

with open(INPUT, encoding="utf-8") as f:
    lines = f.read().splitlines()

i = 0
while i < len(lines):
    if lines[i].startswith("#EXTINF"):
        title = lines[i]
        name = title.split(",")[-1].strip()

        tvg_id = guess_tvg_id(name)
        # 替换 EXTINF
        title = title.replace(
            "#EXTINF:-1",
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}"'
        )

        out.append(title)
        out.append(lines[i + 1])
        i += 2
    else:
        i += 1

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
