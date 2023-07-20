from bokeh.models import ColumnDataSource, Column, Spacer
from bokeh.plotting import figure, Figure
from bokeh.models.widgets import Select
from bokeh.layouts import row
from bokeh.models import Panel
from itertools import chain
from bokeh.models import FuncTickFormatter


def route_tab(data, filter1: str, filter2: str, key: str, value: str, circle_title: str) -> Panel:
    """
    route_tab function generates a tab to add to current document
    :param data: inout data => DataFrame
    :param filter1: first column to filter data by it
    :param filter2: second column to filter data by it
    :param key: part of data that is grouped for creating charts
    :param value: part of data that chart is created on them
    :param circle_title: title of circle
    :return: new tab => Panel
    """
    def create_dataset(new_filter1: str, new_filter2: str) -> (ColumnDataSource, dict):
        """
        this function is used to draw chart under filters
        :param new_filter1: first new filter chosen by user
        :param new_filter2: second new filter chosen by user
        :return: data that is prepared to plot => ColumnDataSource and filters dictionary
        """
        subset = data[(data[filter1] == new_filter1) & (data[filter2] == new_filter2)]
        unique_keys = list(set(subset[key]))
        xs = []
        ys = []
        dic = {}
        for i, j in enumerate(unique_keys):
            keys = subset[subset[key] == j]
            xs.append(list(keys[value]))
            ys.append([i for _ in range(len(keys))])
            dic[i] = j
        xs = list(chain(*xs))
        ys = list(chain(*ys))
        return ColumnDataSource(data={'x': xs, 'y': ys}), dic

    def create_plot(src: ColumnDataSource, dic: dict) -> Figure:
        """
        create circle plot from ColumnDataSource and filters dict
        :param: data source
        :return: Figure
        """
        fig = figure(plot_width=650, plot_height=650, x_axis_label=value.title(),
                     y_axis_label=key.title(), title=circle_title)
        fig.circle('x', 'y', source=src, size=5)
        fig.yaxis[0].ticker.desired_num_ticks = len(dic)
        fig.yaxis.formatter = FuncTickFormatter(
            code="""
            var labels = %s;
            return labels[tick];
            """ % dic
        )
        return fig

    def update(attr, old, new):
        fil1 = filter1_selected.value
        fil2 = filter2_selected.value
        new_src, new_dic = create_dataset(fil1, fil2)
        source.data.update(new_src.data)
        p.yaxis[0].ticker.desired_num_ticks = len(new_dic)
        p.yaxis.formatter = FuncTickFormatter(
            code="""
            var labels = %s;
            return labels[tick];
            """ % new_dic
        )

    filters1 = list(set(data[filter1]))
    filters2 = list(set(data[filter2]))

    filter1_selected = Select(title=filter1.title(), value=data[filter1][0], options=filters1)
    filter2_selected = Select(title=filter2.title(), value=data[filter2][0], options=filters2)
    filter1_selected.on_change('value', update)
    filter2_selected.on_change('value', update)

    filter1_init = filter1_selected.value
    filter2_init = filter2_selected.value

    source, my_dict = create_dataset(filter1_init, filter2_init)
    p = create_plot(source, my_dict)
    return Panel(child=row(Column(filter1_selected, filter2_selected), Spacer(width=100), p), title="Filtering Panel")
