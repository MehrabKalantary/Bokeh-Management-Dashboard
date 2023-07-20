from bokeh.io import curdoc  # current document that loads on server (page)
from bokeh.models.widgets import Tabs  # use tabs to show multiple charts
import pandas as pd  # read data
from hist import hist_tab
from table import table_tab
from route import route_tab
from bokeh.models import Model

directory = "flights.csv"
data = pd.read_csv(directory, index_col=0).dropna()


def modify():
    tab_hist = hist_tab(data, key="airline", value="arrival delay", hist_title="Arrival Delay", start=-60, end=120)
    tab_table = table_tab(data, key="airline", value="arrival delay", table_title="Arrival Delay For Airlines")
    tab_route = route_tab(data, filter1="origin", filter2="destination", key="airline",
                          value="arrival delay", circle_title="Arrival Delay For Airlines")
    return Tabs(tabs=[tab_hist, tab_table, tab_route])


for model in modify().select({'type': Model}):
    prev_doc = model.document
    model._document = None
    if prev_doc:
        prev_doc.remove_root(model)

curdoc().add_root(modify())
