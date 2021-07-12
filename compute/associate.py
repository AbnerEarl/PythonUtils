import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# 数据集处理方法，一般是把所有的商品名称用逗号拼接在一起，再用get_dummies(",")方法进行转换为标准数据集
# 自定义购物数据集
data = {
    'ID': [1, 2, 3, 4, 5, 6],
    "Onion": [1, 0, 0, 1, 1, 1],
    "Potato": [1, 1, 0, 1, 1, 1],
    "Burger": [1, 1, 0, 0, 1, 1],
    "Milk": [0, 1, 1, 1, 0, 1],
    "Beer": [0, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)
df = df[["ID", "Onion", "Potato", "Burger", "Milk", "Beer"]]
print(df)

# 设置支持度来选择频繁项集，选择最小支持度为50%
frequent_item_sets = apriori(df=df, min_support=0.50, use_colnames=True)
print(frequent_item_sets)

# 配置计算规则，指定不同的衡量标准与最小阈值，置信度或者提升度阈值设为1
rules = association_rules(frequent_item_sets, metric="lift", min_threshold=1)
print(rules)

# 根据业务需要进行规则筛选，提升度和置信度都满足
rule1 = rules[(rules["lift"] > 1.125) & (rules["confidence"] > 0.8)]
print(rule1)
