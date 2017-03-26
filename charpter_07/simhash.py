from simhash import Simhash

str0 = 'The Apache Hadoop software library is a framework that allows for the distributed processing large data'
str1 = 'The Apache Hadoop software library is a framework that allows for the distributed processing big data'

# 构造 SimHash 对象
sh0 = Simhash(str0)
sh1 = Simhash(str1)

# 构造特征值，关键字加权
features = [('Apache', 10),('Hadoop', 15),('framework', 3), ('distributed', 10), ('data', 6)]
# 不加权计算
sh0.distance(sh1)
# 加权计算海明距离
sh0.build_by_features(features)
sh1.build_by_features(features)
sh0.distance(sh1)