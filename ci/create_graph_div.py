import pandas as pd
import plotly
import plotly.express
import sys


def get_plot_div(df, graph_title):
    fig = plotly.express.line(
        df,
        x='Date',
        y='Deaths',
        line_group='Country',
        color='Country'
    )

    fig.update_layout(
        title={
            'text': graph_title,
            'font_size': 24
        },
        xaxis={'tickformat': '%d %B<br>%Y (%a)'}
    )

    fig.update_traces(mode='lines+markers')

    show_traces = [
        'Australia:Australia Provinces Sum',
        'Canada:Canada Provinces Sum',
        'China:China Provinces Sum',
        'Czechia:Main',
        'France:Main',
        'Germany:Main',
        'Ireland:Main',
        'Italy:Main',
        'Spain:Main',
        'United Kingdom:Main',
        'US:Main'
    ]

    for trace in fig['data']:
        trace.line.dash = 'dot'
        if trace.name not in show_traces:
            trace.visible = 'legendonly'
        if trace.name == 'China:China Provinces Sum':
            trace.line.color = 'grey'

    return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')


def write_graph_div_file(source_csv_file, graph_title, output_div_file):
    div = get_plot_div(pd.read_csv(source_csv_file), graph_title)

    with open(output_div_file, 'w') as file:
        file.write(div)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise ValueError('usage: source_csv_file graph_title output_file')

    write_graph_div_file(sys.argv[1], sys.argv[2], sys.argv[3])
