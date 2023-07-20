from bokeh.models import ColumnDataSource, Panel, Column, Div
from bokeh.models.widgets import TableColumn, DataTable
from pandas import DataFrame

# table columns for table reindexing
columns = [
    TableColumn(field='', title=''),
    TableColumn(field='count', title=''),
    TableColumn(field='mean', title='Mean'),
    TableColumn(field='std', title='Standard Deviation'),
    TableColumn(field='min', title='Minimum'),
    TableColumn(field='25%', title='Quantile 25%'),
    TableColumn(field='50%', title='Quantile 50%'),
    TableColumn(field='75%', title='Quantile 75%'),
    TableColumn(field='max', title='Maximum'),
]


def table_tab(data: DataFrame, key: str, value: str, table_title: str) -> Panel:
    """
    table_tab function generates a tab to add to current document
    :param data: inout data => DataFrame
    :param key: part of data that is grouped for creating charts
    :param value: part of data that chart is created on them
    :param table_title: title of table
    :return: new tab => Panel
    """
    columns[0].field = key
    columns[0].title = key.title()
    columns[1].title = "Number Of " + key.title() + "s"
    described_data = data.groupby(key)[value].describe()
    described_data['mean'] = described_data['mean'].round(1)
    described_data['std'] = described_data['std'].round(1)
    described_data = described_data.reset_index()
    src = ColumnDataSource(described_data)
    data_table = DataTable(source=src, columns=columns, width=1400, height=1200)
    div = Div(text=table_title, width=1400, height=35)
    column = Column(div, data_table)
    tab = Panel(child=column, title="Table Panel")
    return tab
