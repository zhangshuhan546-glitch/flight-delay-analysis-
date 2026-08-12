import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/Peter/Desktop/Aviation-Data-Analysis/data/FixedDelayedFlights.csv")
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',20)

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
#1.数据体量和结构
print('数据的行数和列数是',df.shape)
print('字段列表:',df.columns.tolist())
print('缺失值情况是')
print(df.isnull().sum())
#2.核心延误指标的整体分布
print('到达延误，起飞延误的整体统计：')
print(df[['DepDelay','ArrDelay']].describe())
#3.延误率（用阈值切出是/否）
df['is_delay_15'] = (df['ArrDelay'] > 15 ).astype(int)
print('全部到达航班的延误率是：',df['is_delay_15'].mean().round(2))
print('ArrDelay小于零的数目',(df['ArrDelay']<=0).sum())
print('DepDelay小于零的数目',(df['DepDelay']<=0).sum())
#4.分类变量的现状
print('航司的种类及数目：')
print(df['UniqueCarrier'].value_counts())
print('出发机场的种类数',df['Origin'].nunique())
print('到达机场的种类数',df['Dest'].nunique())
print('是否取消：')
print(df['Cancelled'].value_counts())
print('是否备降：')
print(df['Diverted'].value_counts())
# 5.时间维度
print('年份分布')
print(df['Year'].value_counts())
print('月份分布')
print(df['Month'].value_counts().sort_index())
print('星期几分布')
print(df['DayOfWeek'].value_counts().sort_index())
#6.航司种类
print('航司的种类数目有：',df['UniqueCarrier'].nunique())
print('各航司航班数量是：')
print(df['UniqueCarrier'].value_counts())
#7.机场种类
print('出发机场的种类数',df['Origin'].nunique())
print('到达机场的种类数',df['Dest'].nunique())
'''描述性得到的结论是 
 1.数据一共有192万行 30列数据
 2.无缺失值
 3.出发和到达的平均延误分别是 43，42 分钟
 4.到达的有20万条数据<0 出发的有0 证明在飞行过程中有20个延误被追回
 5.航司的航班数有的很多，如WN航司有37万，而AQ的只有744条，有的很少 少的不具备普遍性 不符合大数定律
 6.没有取消和备降的航班
 7.都是2008年的航班 12月的航班最多 9月的航班最少'''
#每家航司的延误率及其航班数量
carrier_delay =df.groupby('UniqueCarrier').agg(
    delay_rate = ('is_delay_15','mean'),
    flight_count = ('is_delay_15','count')
).sort_values("delay_rate",ascending=False)
print('各航司的延误率（从高到低排列）')
print(carrier_delay)
#基准：全体航班的平均延误率
avg_delay_rate = df['is_delay_15'].mean().round(2)
print('全体平均延误率：',avg_delay_rate)
print('高于平均延误时间的航司占比为：',(carrier_delay['delay_rate']>avg_delay_rate).astype(int).mean().round(2))
# 60% 的航司延误率高于平均，说明延误不是集中在个别航司，而是普遍偏高；但航司间仍有差距（最高 74% vs 最低 43%），高延误航司的运营问题依然值得关注。
#延误率高且样本数够多的航司
delay_cause = df[['WeatherDelay','CarrierDelay','NASDelay','SecurityDelay', 'LateAircraftDelay']].mean()
#YV航司各个列的平均值
YV_carrier_delay= df[df['UniqueCarrier'] == 'YV'][['WeatherDelay','CarrierDelay','NASDelay','SecurityDelay','LateAircraftDelay']].mean()
print('YV航司各个延误原因的平均值：')
print(YV_carrier_delay)
#YV航司各个延误原因的占比
print('YV航司各个延误原因占比：')
print(YV_carrier_delay/YV_carrier_delay.sum().round(2))
#每个航司的延误原因的延误平均值
print('全部航司的延误原因的延误平均值:')
print(delay_cause.round(2))
#每个航司的原因占比
print('全部航司的延误原因占比:')
print(delay_cause/delay_cause.sum().round(2))
#绘图 YV航司
x = YV_carrier_delay.index
y = YV_carrier_delay.values
plt.pie(y,labels=x,autopct='%1.1f%%')
plt.title('YV航司各延误原因占比')
plt.savefig('C:/Users/Peter/Desktop/Aviation-Data-Analysis/images/YV航司各延误原因占比.png', dpi=150)
plt.show()
#全部航司
x = delay_cause.index
y = delay_cause.values
plt.pie(y,labels=x,autopct='%1.1f%%')
plt.title('全部航司的延误原因占比')
plt.savefig('C:/Users/Peter/Desktop/Aviation-Data-Analysis/images/全部航司的延误原因占比.png', dpi=150)
plt.show()
