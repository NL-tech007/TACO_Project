# ==============================

# TACO 第1次课 示例4

# TACO 言论迷你分类器

# 文件名：mini_classifier.py

# ==============================

 

# 强硬言论关键词

hard_words = [

    "tariff",       # 关税

    "ban",          # 禁止

    "sanction",     # 制裁

    "punish",       # 惩罚

    "threat",       # 威胁

    "impose",       # 施加

    "increase",     # 增加
    
    "fight",        # 打击

    "demand",       # 要求

    "dominate",     # 主导

    "destroyed",    # 摧毁

    "enemy",        # 敌人

    "attack",       # 攻击

    "rigged",       # 不公正的

    "catastrophe",  # 灾难

    "bad",          # 坏

    "disaster",     # 灾难

    "radical",      # 激进

    "worst",        # 最坏

    "terrible",     # 糟糕

    "stupid"        # 愚蠢

]

 

# 软化信号关键词

soft_words = [

    "delay",        # 推迟

    "pause",        # 暂停

    "negotiate",    # 谈判

    "talk",         # 对话

    "consider",     # 考虑

    "may",          # 可能

    "adjust",       # 调整

    "agreement",    # 协议

    "cooperate",    # 合作

    "perhaps",      # 也许

    "fair",         # 公平 

    "open",         # 开放

    "improve",      # 改进

    "settle",       # 解决

    "hopefully",    # 希望

    "good",         # 好

    "better",       # 更好

    "great",        # 很好

    "considering"   # 考虑到

]

 
detected_hard = {}
detected_soft = {}


# 用户输入一句英文财经 / 政治言论

text = input("请输入一句英文言论：")

 

# 转成小写，方便匹配关键词

text_lower = text.lower()

 

# 初始分数

hard_score = 0

soft_score = 0

 

# 检查强硬关键词出现了几个

for word in hard_words:

    if word in text_lower:

        hard_score += 1

        detected_hard[word] = detected_hard.get(word, 0) + 1

 

# 检查软化关键词出现了几个

for word in soft_words:

    if word in text_lower:

        soft_score += 1

        detected_soft[word] = detected_soft.get(word, 0) + 1

 

# 输出打分

print("\n分析结果：")

print()

print("强硬分数：", hard_score)

print("软化分数：", soft_score)

print()

print("检测到的强硬关键词：", detected_hard)

print("检测到的软化关键词：", detected_soft)

print()

 
# 根据分数比例判断分数比例


total = hard_score + soft_score
hard_ratio = hard_score / total if total > 0 else 0
soft_ratio = soft_score / total if total > 0 else 0

if total == 0:
    print("判断：暂时无法判断，需要更多上下文")

elif 1 >= hard_ratio >= 0.90:
    print("强硬度：", hard_ratio * 100, "%")
    print("判断：非常强硬言论")

elif 0.90 > hard_ratio >= 0.55:
    print("强硬度：", hard_ratio * 100, "%")
    print("判断：偏强硬言论")

elif 0.55 > hard_ratio >= 0.50:
    print("强硬度：", hard_ratio * 100, "%")
    print("判断：中性言论")

elif 0.50 > hard_ratio >= 0.10:
    print("强硬度：", hard_ratio * 100, "%")
    print("判断：偏软化言论")

elif 0.10 > hard_ratio >= 0:
    print("强硬度：", hard_ratio * 100, "%")
    print("判断：非常软化言论")
