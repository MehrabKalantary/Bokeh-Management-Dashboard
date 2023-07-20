from bokeh.palettes import Category20_16  # used for colors
from bokeh.models.widgets import CheckboxGroup
import numpy as np
from bokeh.models import ColumnDataSource, Spacer
from bokeh.plotting import figure, Figure
from bokeh.models.widgets import Slider, RangeSlider
from bokeh.layouts import row, Column
from bokeh.models import Panel
import pandas as pd
from pandas import DataFrame


def hist_tab(data: DataFrame, key: str, value: str, hist_title: str, start, end) -> Panel:
    """
    hist_tab function generates a tab to add to current document
    :param data: inout data => DataFrame
    :param key: part of data that is grouped for creating charts
    :param value: part of data that chart is created on them
    :param hist_title: title of hist
    :param start: start point
    :param end: end point
    :return: new tab => Panel
    """
    def create_dataset(active_checkboxes_names: list,
                       start_range=start, end_range=end, hist_bins=10) -> ColumnDataSource:
        """
        this function is used to create active charts
        :param active_checkboxes_names: active checkboxes
        :param start_range: start point
        :param end_range: end point
        :param hist_bins: bins
        :return: data that is prepared to plot => ColumnDataSource
        """
        d = DataFrame(columns=['proportion', 'left', 'right', 'f_proportion', 'f_interval', key, 'color'])
        total_range = end_range - start_range
        for i, name in enumerate(active_checkboxes_names):
            subset = data[data[key] == name]
            arr_hist, edge = np.histogram(subset[value], bins=int(total_range / hist_bins),
                                          range=(start_range, end_range))
            arr_df = DataFrame({
                'proportion': arr_hist / np.sum(arr_hist), 'left': edge[:-1], 'right': edge[1:]
            })
            arr_df['f_proportion'] = ['%0.5f' % po for po in arr_df['proportion']]
            arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(arr_df['left'],
                                                                                              arr_df['right'])]
            arr_df[key] = name
            arr_df['color'] = Category20_16[i]
            d = pd.concat([d, arr_df])
        d = d.sort_values([key, 'left'])
        return ColumnDataSource(d)

    def create_plot(data_source: ColumnDataSource) -> Figure:
        """
        create histogram from ColumnDataSource
        :param data_source
        :return: Figure
        """
        fig = figure(plot_width=650, plot_height=650, title=hist_title)
        fig.quad(source=data_source, bottom=0, top='proportion', left='left', right='right', color='color',
                 fill_alpha=0.7, legend_field=key)
        return fig

    def update(attr, new, old):
        """ updating charts after pressing checkboxes, or sliders after changing them """
        active_checkboxes = [checkbox.labels[i] for i in checkbox.active]  # list of active checkboxes
        ds = create_dataset(active_checkboxes, range_slider.value[0], range_slider.value[1], bins_slider.value)
        src.data.update(ds.data)

    unique_keys = list(set(data[key]))
    unique_keys.sort()
    colors = list(Category20_16)
    colors.sort()

    checkbox = CheckboxGroup(labels=unique_keys, active=[0])
    checkbox.on_change('active', update)

    bins_slider = Slider(start=1, end=30, step=1, value=5, title="Bins Slider")
    bins_slider.on_change('value', update)

    range_slider = RangeSlider(start=start, end=end, value=(start, end), step=5, title='Range')
    range_slider.on_change('value', update)

    init_data = [checkbox.labels[i] for i in checkbox.active]
    src = create_dataset(init_data)
    p = create_plot(src)
    column = Column(checkbox, Spacer(height=50), bins_slider, Spacer(height=20), range_slider)
    layout = row(column, Spacer(width=100), p)
    return Panel(child=layout, title='Histogram Panel')
