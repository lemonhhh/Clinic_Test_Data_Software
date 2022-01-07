from pyecharts import options as opts
from pyecharts.charts import Map, Page
from pyecharts.faker import Collector, Faker

def readData(path):
    populations = list()
    with open(path,"rt",encoding="utf8") as f:#读取中文文本文件
        line = f.readline()
        while line:
            a = line[:-1].split("\t")
            populations.append([a[0],int(a[1])])
            line = f.readline()
    return populations

C = Collector()
@C.funcs
def map_visualmap() -> Map:
    c = (
        Map()
        .add("中华人民共和国各省人口数(第6次人口普查)", populations, "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="pyecharts 嵌入 PyQt5 DEMO"),
            visualmap_opts=opts.VisualMapOpts(max_=max_),
        )
    )
    return c
populations = readData("人口.txt")#从国家统计局官网下载
max_ = max(x[1] for x in populations)
Page().add(*[fn() for fn, _ in C.charts]).render("ChinaPopulationMap.html")