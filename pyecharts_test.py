from pyecharts.charts import Bar
from pyecharts import options as opt
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot
from pyecharts.globals import ThemeType


def try_bar():
    x_data = ['jan', 'feb', 'mar', 'apr', 'may']
    y_data = [10, 20, 15, 25, 30]

    # 创建柱状图
    # bar_chart = Bar()  # 最简单创建
    bar_chart = Bar(init_opts=opt.InitOpts(theme=ThemeType.ROMA))  # 试试其他theme
    bar_chart.add_xaxis(x_data)
    bar_chart.add_yaxis('sales', y_data)

    # 配置图表
    bar_chart.set_global_opts(
        title_opts=opt.TitleOpts(title='bar chart of monthly sales'),
        xaxis_opts=opt.AxisOpts(name='month'),
        yaxis_opts=opt.AxisOpts(name='sales (10k)'),
        legend_opts=opt.LegendOpts(pos_left='center', pos_top='top'),
        toolbox_opts=opt.ToolboxOpts()  # 显示工具
    )

    # 渲染图表
    # bar_chart.render('chart_1.html')  # 生成html文件
    make_snapshot(snapshot, bar_chart.render('chart_1.html'), 'chart_1.png')  # 生成html和png文件


if __name__ == '__main__':
    try_bar()
