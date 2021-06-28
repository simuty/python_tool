from typing import List
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
import json
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
import time, datetime

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://echarts.apache.org/examples/editor.html?c=line-stack

目前无法实现的功能:

暂无
"""


x_data = [x for x in range(8)]


def cal(total, stake):
    start = 1
    count = 0
    #
    tmp = {
        "oneST": [],
        "st1000": [],
        "dayOf1000": [],
        "total": []
    }
    st_total = 0
    while (start < 9):
        oneST = total / stake
        st1000 = oneST * 1000
        dayOf1000 = st1000 / 7
        total = total / 2
        start = start + 1
        count = oneST + count
        tmp["oneST"].append(oneST)
        tmp["st1000"].append(st1000)
        tmp["dayOf1000"].append(dayOf1000)
        tmp["total"].append(total)

        st_total = oneST + st_total
        # print(st_total)
        # print(
        #     "1000个： 第 周 1st: ",
        #     total,
        #     total / 7,
        #     oneST,
        #     "==>>>> 1000st total/day",
        #     st1000,
        #     dayOf1000,
        # )
    tmp["st_total"] = [st_total for i in range(8)]
    return tmp


total_st_tdog = 75000000
stake_t_t = 6500000

total_st = 6500000
stake_t = 650000


def line_markpoint() -> Line:
    c = (
        Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="t",
            stack="总量",
            y_axis=cal(total_st, stake_t)["oneST"],
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
        )
        .add_yaxis(
            series_name="st",
            stack="总量",
            y_axis=cal(total_st_tdog, stake_t_t)["oneST"],
            label_opts=opts.LabelOpts(is_show=False),
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[
            #         opts.MarkPointItem(type_="max", name="最大值"),
            #         opts.MarkPointItem(type_="min", name="最小值"),
            #     ]
            # ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="折线图堆叠"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                # axistick_opts=opts.AxisTickOpts(is_show=True),
                # splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


def read_json():
    with open("data.json") as json_file:
        config = json.load(json_file)
        return config["data"]["dayList"]
        # print(config["data"]["dayList"])


def test_bar() -> Bar:
    data = read_json()
    # print(data)

    # nodes = [
    # {
    #     "time": node["time"],
    #     "price": node["price"],
    #     "eachHaveCoin": node["eachHaveCoin"],
    #     "eachHaveUsdt": node["eachHaveUsdt"],
    #     "eachHaveCny": node["eachHaveCny"],
    # }
    # for node in data
    # ]

    time_list, price_list, eachHaveCoin_list = [], [], []
    for node in data:
        time_list.append(node["time"])
        price_list.append(node["price"])
        eachHaveCoin_list.append(node["eachHaveCoin"])

    c = (
        Bar({"theme": ThemeType.MACARONS})
        .add_xaxis(time_list)
        .add_yaxis("", price_list)
        .add_yaxis("商家B", eachHaveCoin_list)
        .set_global_opts(
            title_opts={"text": "Bar-通过 dict 进行配置",
                        "subtext": "我也是通过 dict 进行配置的"}
        )
    )
    return c



def test_line() -> Line:
    data = read_json()
    time_list, price_list, eachHaveCoin_list, eachHaveUsdt_list = [], [], [], []
    for node in data:

        timeArray = time.localtime(node["time"]/1000)

        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        time_list.append(otherStyleTime)
        price_list.append(float(node["price"]))
        eachHaveCoin_list.append(node["eachHaveCoin"])
        eachHaveUsdt_list.append(node["eachHaveUsdt"])

    print(time_list)
    print(price_list)
    c = (
        Line()
        .add_xaxis(xaxis_data=time_list)
        # .add_yaxis(
        #     series_name="eachHaveCoin",
        #     stack="eachHaveCoin",
        #     y_axis=eachHaveCoin_list,
        #     label_opts=opts.LabelOpts(is_show=False),
        #     markline_opts=opts.MarkLineOpts(
        #         data=[opts.MarkLineItem(type_="average", name="平均值")]
        #     ),
        # )
        # .add_yaxis(
        #     series_name="price",
        #     stack="price",
        #     y_axis=price_list,
        #     label_opts=opts.LabelOpts(is_show=False),
        #     markpoint_opts=opts.MarkPointOpts(
        #         data=[
        #             opts.MarkPointItem(type_="max", name="最大值"),
        #             opts.MarkPointItem(type_="min", name="最小值"),
        #         ]
        #     ),
        #     markline_opts=opts.MarkLineOpts(
        #         data=[opts.MarkLineItem(type_="average", name="平均值")]
        #     ),
        # )
        .add_yaxis(
            series_name="eachHaveUsdt",
            stack="eachHaveUsdt",
            y_axis=eachHaveUsdt_list,
            label_opts=opts.LabelOpts(is_show=False),
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
            title_opts=opts.TitleOpts(title="折线图堆叠"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            # xaxis_opts=opts.AxisOpts(type_="time", axislabel_opts=opts.LabelOpts(rotate=-15)),
            # xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c