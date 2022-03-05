from pyecharts import options as opts
from pyecharts.charts import Liquid
from pyecharts.commons.utils import JsCode

result=[0.9961599]

def generate_data(result):
    c = (
        Liquid()
        .add(
            "疾病风险",
            result,
            label_opts=opts.LabelOpts(
                font_size=50,
                formatter=JsCode(
                    """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
                ),
                position="inside",
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Liquid-数据精度"))
        .render("liquid_data_precision.html")
    )

print(type(result))
generate_data(result)