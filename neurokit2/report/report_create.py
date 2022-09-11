# -*- coding: utf-8 -*-
import inspect
import numpy as np
import pandas as pd

from ..ppg import ppg_plot

# TODO: comments


def report_create(
    filename="myreport.html", signals=None, report_info={"sampling_rate": 1000}
):
    description, ref = describe_processing(report_info)
    summary_table = summary_table_create(signals)
    fig = ppg_plot(signals, sampling_rate=report_info["sampling_rate"], static=False)
    contents = [description, summary_table, fig, ref]
    html_combine(contents=contents, filename=filename)


def describe_processing(report_info):
    # TODO: automate references?
    description = "<br><b>Description</b><br>"
    for key in ["text_cleaning", "text_method"]:
        if key in report_info.keys():
            description += report_info[key] + "<br>"
    ref = "<br><b>References</b><br>"

    if "references" in report_info.keys():
        for reference in report_info["references"]:
            ref += reference + "<br>"
    return description, ref


def summary_table_create(signals):
    summary = {}
    summary["PPG_Rate_Mean"] = np.mean(signals["PPG_Rate"])
    summary["PPG_Rate_SD"] = np.std(signals["PPG_Rate"])
    summary_table = pd.DataFrame(summary, index=[0])  # .transpose()
    print(summary_table.to_markdown(index=None))
    return "<br> <b>Summary table</b> <br>" + summary_table.to_html(index=None)


def html_combine(contents=[], filename="myreport.html"):
    # https://stackoverflow.com/questions/59868987/plotly-saving-multiple-plots-into-a-single-html
    with open(filename, "w") as page:
        page.write("<html><head></head><body>" + "\n")
        for content in contents:
            if isinstance(content, str):
                inner_html = content
            else:
                inner_html = content.to_html().split("<body>")[1].split("</body>")[0]
            page.write(inner_html)
            page.write("<br>")
        page.write("</body></html>" + "\n")


def get_default_args(func):
    # https://stackoverflow.com/questions/12627118/get-a-function-arguments-default-value
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }
