import pyecharts.options as opts
from pyecharts.charts import Line



week_name_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
high_temperature = [11, 11, 15, 13, 12, 13, 10]
low_temperature = [1, -2, 2, 5, 3, 2, 0]


(
    Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
    .add_xaxis(xaxis_data=week_name_list)
    .add_yaxis(
        series_name="最高气温",
        y_axis=high_temperature,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="未来一周气温变化", subtitle="纯属虚构"),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
    .render("temperature_change_line_chart.html")
)

