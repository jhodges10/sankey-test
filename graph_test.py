import plotly.plotly as py
import urllib, json


def draw_graph():
    data_trace = dict(
        type='sankey',
        width=1118,
        height=772,
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        orientation="h",
        valueformat=".0f",
        valuesuffix="TWh",
        node=dict(
            pad=15,
            thickness=15,
            line=dict(
                color="black",
                width=0.5
            ),
            label=data['data'][0]['node']['label'],
            color=data['data'][0]['node']['color']
        ),
        link=dict(
            source=data['data'][0]['link']['source'],
            target=data['data'][0]['link']['target'],
            value=data['data'][0]['link']['value'],
            label=data['data'][0]['link']['label']
        ))

    layout = dict(
        title="Sankey Diagram Test for Tracking Dash Transactions",
        font=dict(
            size=10
        )
    )

    fig = dict(data=[data_trace], layout=layout)
    py.iplot(fig, validate=False)
