import pandas as pd
from pyecharts.charts import Scatter
from pyecharts import options as opts
import seaborn as sns
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot

# 加载钻石数据集
# diamonds = sns.load_dataset('diamonds')
diamonds = sns.load_dataset('diamonds', data_home='seaborn-data', cache=True)  # 太慢了，直接用本地的

# 定义颜色映射
color_map = {
    'I1': '#A63130', 'SI2': '#D54A38', 'SI1': '#EDB74D',
    'VS2': '#000000', 'VS1': '#A0B87B', 'VVS2': '#46966E',
    'VVS1': '#306884', 'IF': '#7D7D7D'
}

# 将depth分成6个类别，并映射到点的大小
diamonds['depth_category'] = pd.qcut(diamonds['depth'], 6, labels=False)
# 将类别映射到一组具体的大小
size_map = {i: size for i, size in enumerate([3, 4, 5, 6, 7, 8])}
diamonds['size'] = diamonds['depth_category'].map(size_map)

# 创建散点图对象
scatter = Scatter(init_opts=opts.InitOpts(width="800px", height="600px"))

# 设置全局选项
scatter.set_global_opts(
    title_opts=opts.TitleOpts(title="Diamonds"),
    legend_opts=opts.LegendOpts(pos_right="3%", pos_bottom="3%"),  # 似乎难以在图例中表达depth，暂时搁置这一问题
    tooltip_opts=opts.TooltipOpts(formatter="{a} <br/>{b}: {c}"),
    xaxis_opts=opts.AxisOpts(name="carat", type_="value"),  # 这个type_很重要，保证坐标轴是依照数值有序增长的
    yaxis_opts=opts.AxisOpts(name="price", type_="value"),
)

# 逐一添加数据点
for clarity, group in diamonds.groupby('clarity'):
    scatter.add_xaxis(group['carat'].tolist())
    scatter.add_yaxis(
        series_name=clarity,
        y_axis=[opts.ScatterItem(value=[x[0], x[1]], symbol_size=x[2]) for x in zip(group['carat'], group['price'], group['size'])],
        label_opts=opts.LabelOpts(is_show=False),
        itemstyle_opts=opts.ItemStyleOpts(color=color_map[clarity])
    )

# 渲染图表
make_snapshot(snapshot, scatter.render('diamonds.html'), 'diamonds.png')
