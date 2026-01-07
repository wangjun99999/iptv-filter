import requests
import re

# --------------------- 配置 ---------------------

SRC_URL = "https://raw.githubusercontent.com/q1017673817/iptvz/refs/heads/main/zubo_all.m3u"

# 地方台 tvg-id 映射
LOCAL_TVG = {
    "CCTV-1综合": "CCTV1",
    "CCTV-2财经": "CCTV2",
    "CCTV-3综艺": "CCTV3",
    "CCTV-4中文国际": "CCTV4",
    "CCTV-4 欧洲": "CCTV4欧洲",
    "CCTV-4欧洲": "CCTV4欧洲",
    "CCTV-4 北美": "CCTV4美洲",
    "CCTV-4美洲": "CCTV4美洲",
    "CCTV-5体育": "CCTV5",
    "CCTV-5+体育赛事": "CCTV5+",
    "CCTV-6电影": "CCTV6",
    "CCTV-7国防军事": "CCTV7",
    "CCTV-8电视剧": "CCTV8",
    "CCTV-9纪录": "CCTV9",
    "CCTV-10科教": "CCTV10",
    "CCTV-11戏曲": "CCTV11",
    "CCTV-12社会与法": "CCTV12",
    "CCTV-13新闻": "CCTV13",
    "CCTV-14少儿": "CCTV14",
    "CCTV-15音乐": "CCTV15",
    "CCTV-16奥林匹克": "CCTV16",
    "CCTV-17农业农村": "CCTV17",
    "山东体育频道": "山东体育",
    "山东体育休闲": "山东体育",
    "山东农科频道": "山东农科",
    "山东少儿频道": "山东少儿",
    "山东教育频道": "山东教育",
    "山东教育卫视": "山东教育",
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
    "北京体育休闲": "BTV体育",
    "北京影视频道": "BTV影视",
    "北京文艺频道": "BTV文艺",
    "北京新闻频道": "BTV新闻",
    "北京生活频道": "BTV生活",
    "北京纪实科教": "BTV科教",
    "北京财经频道": "BTV财经",
    "北京卡酷少儿": "卡酷少儿",
    "广东体育频道": "广东体育",
    "辽宁体育休闲": "辽宁体育",
    "天津体育频道": "天津体育",
    "武汉文体频道": "武汉文体",
    "陕西体育休闲": "陕西七套",
    "江苏体育休闲": "江苏休闲体育",
    "成都公共频道": "CDTV5",
    "云南康旅频道": "云南康旅",
    "福建文体频道": "福建体育频道",
    "杭州青少": "杭州HTV5", 
}

# 4K 超高清频道（精确匹配）
FOUR_K_CHANNELS = {
    "四川联通": ["CCTV4K超高清"],
    "河北联通": ["CCTV4K超高清", "北京卫视4K超高清"],
    "广东联通": ["广东4K超高清"],
}

# 体育频道
SPORTS_CHANNELS = {
    "广东联通": ["广东体育频道"],
    "重庆联通": ["重庆文体娱乐"],
    "辽宁联通": ["辽宁体育休闲"],
    "天津联通": ["天津体育频道"],
    "广东电信": ["深圳体育健康"],
    "重庆电信": ["重庆文体娱乐"],
    "福建电信": ["福建文体频道"],
    "湖北电信": ["武汉文体频道"],
    "陕西电信": ["陕西体育休闲"],
    "天津电信": ["天津体育频道"],
    "江苏电信": ["江苏体育休闲"],
    "上海电信": ["五星体育"],
    "四川电信": ["成都公共频道"],
    "云南电信": ["云南康旅频道"],
    "浙江电信": ["杭州青少"],
}

# tvg-logo 映射示例
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
    "山东体育": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E4%BD%93%E8%82%B2.png",
    "山东农科": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E5%86%9C%E7%A7%91.png",
    "山东少儿": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E5%B0%91%E5%84%BF.png",
    "山东教育": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E6%95%99%E8%82%B2.png",
    "山东文旅": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E6%96%87%E6%97%85.png",
    "山东新闻": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E6%96%B0%E9%97%BB.png",
    "山东生活": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E7%94%9F%E6%B4%BB.png",
    "山东综艺": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E7%BB%BC%E8%89%BA.png",
    "山东齐鲁": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E9%BD%90%E9%B2%81.png",
    "山东居家购物": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%B1%B1%E4%B8%9C%E5%B1%85%E5%AE%B6%E8%B4%AD%E7%89%A9.png",    
    "青岛tv1": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-1.png",
    "青岛tv2": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-2.png",
    "青岛tv3": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-3.png",
    "青岛tv4": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-4.png",
    "青岛tv5": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/QTV-5.png",
    "青岛tv6": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/QTV6.png",
    "BTV体育": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%AC%E4%BD%93%E8%82%B2%E4%BC%91%E9%97%B2.png",
    "BTV影视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%AC%E5%BD%B1%E8%A7%86.png",
    "BTV文艺": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%AC%E6%96%87%E8%89%BA.png",
    "BTV新闻": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%AC%E6%96%B0%E9%97%BB.png",
    "BTV生活": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%AC%E7%94%9F%E6%B4%BB.png",
    "BTV科教": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%AC%E7%BA%AA%E5%AE%9E%E7%A7%91%E6%95%99.png",
    "BTV财经": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%AC%E8%B4%A2%E7%BB%8F.png",
    "卡酷少儿": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8D%A1%E9%85%B7%E5%B0%91%E5%84%BF.png",
    "北京国际频道": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E5%8C%97%E4%BA%AC%E5%9B%BD%E9%99%85%E9%A2%91%E9%81%93.png",
    "北京IPTV4K超清": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%ACIPTV4K.png",
    "北京IPTV淘电影": "https://gitee.com/wuxiyihu/logo/raw/master/tv/bjtdy.png",
    "北京IPTV淘剧场": "https://gitee.com/wuxiyihu/logo/raw/master/tv/bjtjc.png",
    "北京IPTV淘娱乐": "https://gitee.com/wuxiyihu/logo/raw/master/tv/bjtyl.png",
    "北京IPTV淘BABY": "https://gitee.com/wuxiyihu/logo/raw/master/tv/bjtbb.png",
    "北京IPTV萌宠TV": "https://gitee.com/wuxiyihu/logo/raw/master/tv/bjmctv.png",
    "北京卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8C%97%E4%BA%AC%E5%8D%AB%E8%A7%86.png",
    "湖南卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B9%96%E5%8D%97%E5%8D%AB%E8%A7%86.png",
    "东方卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E4%B8%9C%E6%96%B9%E5%8D%AB%E8%A7%86.png",
    "浙江卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B5%99%E6%B1%9F%E5%8D%AB%E8%A7%86.png",
    "江苏卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B1%9F%E8%8B%8F%E5%8D%AB%E8%A7%86.png",
    "深圳卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B7%B1%E5%9C%B3%E5%8D%AB%E8%A7%86.png",
    "广东卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B9%BF%E4%B8%9C%E5%8D%AB%E8%A7%86.png",
    "安徽卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%AE%89%E5%BE%BD%E5%8D%AB%E8%A7%86.png",
    "天津卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%A4%A9%E6%B4%A5%E5%8D%AB%E8%A7%86.png",
    "重庆卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E9%87%8D%E5%BA%86%E5%8D%AB%E8%A7%86.png",
    "山东卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E4%B8%9C%E5%8D%AB%E8%A7%86.png",
    "河北卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B2%B3%E5%8C%97%E5%8D%AB%E8%A7%86.png",
    "辽宁卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E8%BE%BD%E5%AE%81%E5%8D%AB%E8%A7%86.png",
    "湖北卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B9%96%E5%8C%97%E5%8D%AB%E8%A7%86.png",
    "吉林卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%90%89%E6%9E%97%E5%8D%AB%E8%A7%86.png",
    "贵州卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E8%B4%B5%E5%B7%9E%E5%8D%AB%E8%A7%86.png",
    "东南卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E4%B8%9C%E5%8D%97%E5%8D%AB%E8%A7%86.png",
    "江西卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B1%9F%E8%A5%BF%E5%8D%AB%E8%A7%86.png",
    "海南卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B5%B7%E5%8D%97%E5%8D%AB%E8%A7%86.png",
    "黑龙江卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E9%BB%91%E9%BE%99%E6%B1%9F%E5%8D%AB%E8%A7%86.png",
    "云南卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E4%BA%91%E5%8D%97%E5%8D%AB%E8%A7%86.png",
    "四川卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%9B%9B%E5%B7%9D%E5%8D%AB%E8%A7%86.png",
    "宁夏卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%AE%81%E5%A4%8F%E5%8D%AB%E8%A7%86.png",
    "山西卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B1%B1%E8%A5%BF%E5%8D%AB%E8%A7%86.png",
    "广西卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B9%BF%E8%A5%BF%E5%8D%AB%E8%A7%86.png",
    "新疆卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%96%B0%E7%96%86%E5%8D%AB%E8%A7%86.png",
    "河南卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B2%B3%E5%8D%97%E5%8D%AB%E8%A7%86.png",
    "甘肃卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E7%94%98%E8%82%83%E5%8D%AB%E8%A7%86.png",
    "西藏卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E8%A5%BF%E8%97%8F%E5%8D%AB%E8%A7%86.png",
    "陕西卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E9%99%95%E8%A5%BF%E5%8D%AB%E8%A7%86.png",
    "青海卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E9%9D%92%E6%B5%B7%E5%8D%AB%E8%A7%86.png",
    "内蒙古卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%86%85%E8%92%99%E5%8F%A4%E5%8D%AB%E8%A7%86.png",
    "三沙卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E4%B8%89%E6%B2%99%E5%8D%AB%E8%A7%86.png",
    "厦门卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%8E%A6%E9%97%A8%E5%8D%AB%E8%A7%86.png",
    "兵团卫视": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%85%B5%E5%9B%A2%E5%8D%AB%E8%A7%86.png",  
    "CDTV5": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/cdtv5.png",
    "武汉文体": "https://gitee.com/wuxiyihu/logo/raw/master/tv/Wuhan5.png",
    "天津体育": "https://gitee.com/wuxiyihu/logo/raw/master/tv/Tianjin5.png",
    "辽宁体育": "https://gitee.com/wuxiyihu/logo/raw/master/tv/Liaoning6.png",
    "云南康旅": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E4%BA%91%E5%8D%97%E5%BA%B7%E6%97%85.png",
    "杭州HTV5": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E6%9D%AD%E5%B7%9E%E9%9D%92%E5%B0%91.png",     
    "五星体育": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E4%BA%94%E6%98%9F%E4%BD%93%E8%82%B2.png",
    "广东体育": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E5%B9%BF%E4%B8%9C%E4%BD%93%E8%82%B2.png",
    "深圳体育健康": "https://raw.githubusercontent.com/wangjun99999/logo/refs/heads/main/CN/%E6%B7%B1%E5%9C%B3%E4%BD%93%E8%82%B2%E5%81%A5%E5%BA%B7.png",
    "江苏休闲体育": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E6%B1%9F%E8%8B%8F%E4%BC%91%E9%97%B2%E4%BD%93%E8%82%B2.png",
    "福建体育频道": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E7%A6%8F%E5%BB%BA%E6%96%87%E4%BD%93.png",
    "重庆文体娱乐": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E9%87%8D%E5%BA%86%E6%96%87%E4%BD%93%E5%A8%B1%E4%B9%90.png",
    "陕西七套": "https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/%E9%99%95%E8%A5%BF%E4%BD%93%E8%82%B2%E4%BC%91%E9%97%B2.png",   
}

# --------------------- 筛选规则 ---------------------

KEEP_RULES = {
    "山东电信": {
        "cctv": True,
        "satellite": True,
        "keywords": ["山东", "青岛1","青岛2","青岛3","青岛4","青岛5","青岛6"]
    },
    "山东联通": {
        "cctv": True,
        "satellite": True,
        "keywords": ["山东","青岛QTV1","青岛QTV2","青岛QTV3","青岛QTV4"]
    },
    "北京联通": {
        "cctv": True,
        "satellite": True,
        "keywords": ["北京","青岛QTV1","青岛QTV2","青岛QTV3","青岛QTV4"]
    },
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


    # ---------- 4K 频道 ----------
    is_4k = False
    for operator, channels in FOUR_K_CHANNELS.items():
        if group.startswith(operator) and raw_name in channels:
            is_4k = True
            break

    # ---------- 体育频道 ----------
    is_sports = False
    sports_name = ""
    if not is_4k:
        for operator, channels in SPORTS_CHANNELS.items():
            if group.startswith(operator) and raw_name in channels:
                is_sports = True
                sports_name = f"{operator}丨{raw_name}"
                break

    # --------------------- 是否保留 ---------------------
    keep = False

    if is_4k:
        keep = True

    elif is_sports:
        keep = True

    else:
        for prefix, rule in KEEP_RULES.items():
            if group.startswith(prefix):
                if rule.get("cctv") and raw_name.upper().startswith("CCTV"):
                    keep = True
                elif rule.get("satellite") and "卫视" in raw_name:
                    keep = True
                elif "exact" in rule and raw_name in rule["exact"]:
                    keep = True
                elif "keywords" in rule:
                    for kw in rule["keywords"]:
                        if kw in raw_name:
                            keep = True
                            break
                break  # 匹配到分组就不用继续看
    if not keep:
        i += 2
        continue

    tvg_id = guess_tvg_id(raw_name)
    tvg_name = raw_name
    tvg_logo = guess_logo(tvg_id)

    if is_4k:
        extinf_new = (
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" '
            f'tvg-logo="{tvg_logo}" group-title="4K频道",{raw_name}'
        )

    elif is_sports:
        extinf_new = (
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" '
            f'tvg-logo="{tvg_logo}" group-title="体育频道",{sports_name}'
        )

    else:
        extinf_new = (
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" '
            f'tvg-logo="{tvg_logo}" group-title="{group}",{raw_name}'
        )

    out.append(extinf_new)
    out.append(url)
    i += 2

# --------------------- 输出 ---------------------

with open("output_epg.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("生成完成：output_epg.m3u（按规则筛选 + 体育频道 + tvg + logo）")
