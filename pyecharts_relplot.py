from pyecharts import options as opts
from pyecharts.charts import Line, Grid
import seaborn as sns
import pandas as pd
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot

# 加载数据集
data_dots = sns.load_dataset('dots', data_home='seaborn-data', cache=True)

# 定义颜色和线宽的映射
palette_map = {0: '#F6B48F', 3.2: '#F37651', 6.4: '#E13342', 12.8: '#AD1759', 25.6: '#701F57', 51.2: '#35193E'}
choice_size_map = {'T1': 8, 'T2': 1}  # T1为粗线，T2为细线

# 准备两个align类别的图表
charts = []
for align in ['dots', 'sacc']:
    line = Line()
    align_data = data_dots[data_dots['align'] == align]
    for choice in ['T1', 'T2']:
        for coherence in sorted(data_dots['coherence'].unique()):
            # 筛选对应choice和coherence的数据
            filter_data = align_data[(align_data['choice'] == choice) & (align_data['coherence'] == coherence)]
            # 设置折线图的属性
            line.add_xaxis(filter_data['time'].tolist())
            line.add_yaxis(
                series_name=f'{coherence}',
                y_axis=filter_data['firing_rate'].tolist(),
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=choice_size_map[choice]),
                color=palette_map[coherence],  # 根据coherence选择颜色
                label_opts=opts.LabelOpts(is_show=False),
            )
    line.set_global_opts(
        legend_opts=opts.LegendOpts(pos_right="3%", pos_bottom="3%"),  # 还是调整一下图例的位置，因地制宜
        xaxis_opts=opts.AxisOpts(name='time', type_='value'),
        yaxis_opts=opts.AxisOpts(name='firing_rate', type_='value')
    )
    charts.append(line)

# 将两个align的图表放在并列布局
grid = Grid(init_opts=opts.InitOpts(width="1000px", height="600px"))  # 可以调整初始化选项来设置整体布局大小

# 偏移控制，防止元素重叠
align_map = {0: 'dots', 1: 'sacc'}
pos_map = {0: (5, 55), 1: (55, 5)}

for idx, chart in enumerate(charts):
    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=f"Align={align_map[idx]}", pos_left=f"{pos_map[idx][0]}%"),  # 根据子图位置调整标题位置
        yaxis_opts=opts.AxisOpts(min_=0, max_=80, interval=10)  # 控制y轴一致
    )
    grid.add(
        chart,
        grid_opts=opts.GridOpts(
            pos_left=f'{pos_map[idx][0]}%',  # 左偏移
            pos_right=f'{pos_map[idx][1]}%',  # 右偏移
        ),
    )

# 渲染图表
make_snapshot(snapshot, grid.render('dots.html'), 'dots.png')
