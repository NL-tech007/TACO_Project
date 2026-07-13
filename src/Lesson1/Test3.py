# ==============================

# TACO 第1次课 示例3

# 模拟 API：输入代码，返回资产信息

# 文件名：mock_api.py

# ==============================

 

# 这个字典模拟一个外部数据库

market_data = {

    "USO": {

        "name": "United States Oil Fund",

        "type": "Oil ETF",

        "meaning": "常用于观察石油价格变化"

    },

    "GLD": {

        "name": "SPDR Gold Shares",

        "type": "Gold ETF",

        "meaning": "常用于观察黄金和避险情绪"

    },

    "SPY": {

        "name": "S&P 500 ETF",

        "type": "Stock Market ETF",

        "meaning": "常用于观察美国整体股市"

    },

    "QQQ": {

        "name": "Nasdaq 100 ETF",

        "type": "Technology ETF",

        "meaning": "常用于观察科技股表现"

    }

}

 

 

def get_asset_info(symbol):

    """

    根据资产代码返回资产信息。

 

    参数：

        symbol: 资产代码，例如 USO、GLD、SPY、QQQ

 

    返回：

        如果找到，返回资产信息字典；

        如果没找到，返回 None。

    """

 

    if symbol in market_data:

        return market_data[symbol]

    else:

        return None

 

 

# 让用户输入资产代码

user_symbol = input("请输入资产代码，例如 USO / GLD / SPY / QQQ：")

 

# 把用户输入转成大写，避免 uso 和 USO 不一致

user_symbol = user_symbol.upper()

 

# 调用函数，获取资产信息

result = get_asset_info(user_symbol)

 

# 输出结果

if result is None:

    print("没有找到这个资产代码。")

else:

    print("\n查询结果：")

    print("名称：", result["name"])

    print("类型：", result["type"])

    print("含义：", result["meaning"])