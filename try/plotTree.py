import json

from pyecharts import options as opts
from pyecharts.charts import Tree

with open("../disease.json", "r", encoding="utf-8") as f:
    j = json.load(f)
c = (
    Tree()
    .add("", [j], collapse_interval=2, layout="radial")
    .set_global_opts(title_opts=opts.TitleOpts(title="Tree-Layout"))
    .render("tree_layout.html")
)