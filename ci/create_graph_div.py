import pandas as pd
import plotly
import plotly.express
import sys


def get_plot_div(df):
    fig = plotly.express.line(
        df,
        x='Date',
        y='Deaths',
        line_group='Country',
        color='Country'
    )

    fig.update_layout(
        xaxis={'tickformat': '%d %B<br>%Y (%a)'},
        margin=dict(l=25, r=25, b=25, t=25)
    )

    fig.update_traces(mode='lines+markers')

    show_traces = {
        # 'Australia:Australia Provinces Sum': 'yellow',
        # 'Canada:Canada Provinces Sum': 'teal',
        # 'China:China Provinces Sum': 'grey',
        # 'Czechia:Main': 'blue',
        # 'France:Main': 'green',
        # 'Germany:Main': 'gold',
        # 'Ireland:Main': 'lime',
        # 'Italy:Main': 'orange',
        # 'Spain:Main': 'magenta',
        'United Kingdom:Main': 'blue',
        'US:Main': 'red'
    }

    for trace in fig['data']:
        trace.line.dash = 'dot'
        if trace.name in list(show_traces.keys()):
            trace.line.color = show_traces[trace.name]
        else:
            trace.visible = 'legendonly'
            trace.line.color = 'black'

    return fig.to_html(full_html=False, include_plotlyjs=False)


def write_graph_div_file(source_csv_file, output_div_file):
    div = get_plot_div(pd.read_csv(source_csv_file))

    with open(output_div_file, 'w') as file:
        file.write(div)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('usage: source_csv_file output_file')

    write_graph_div_file(sys.argv[1], sys.argv[2])
