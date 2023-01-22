import pandas as pd
import plotly.graph_objects as go 

from data_processor import read_csv


def portfolio_chart(cat_x, cat_y):
    df = read_csv('data/category.csv')
    df2 = read_csv('data/positions.csv')

    ticks = tuple(range(-4, 5))
    blank_ticks = ('', ) * (len(ticks) - 2)
    common_settings = {
        'range': (min(ticks), max(ticks)), 
        'tickmode': 'array', 
        'tickvals': ticks, 
    }

    fig = go.Figure()
    fig.add_hline(y=0, opacity=0.2)
    fig.add_vline(x=0, opacity=0.2)

    data = pd.merge(
        left=df2[df2.CATEGORY == cat_x], 
        right=df2[df2.CATEGORY == cat_y], 
        how='inner', 
        left_on=('TYPE', ), 
        right_on=('TYPE', ), 
        suffixes=('_X', '_Y'), 
    )
    for t, sub in data.groupby('TYPE', sort=False):
        fig.add_scatter(
            x=list(sub.POSITION_X), 
            y=list(sub.POSITION_Y), 
            mode='markers', 
            hoverinfo='text', 
            hovertext=f"{t}", 
            name=t, 
            marker=dict(
                size=20,
                opacity=0.7, 
            ), 
        )
    fig.update_layout(
        width=650, 
        height=650, 
        xaxis=dict(
            title=df.loc[cat_x].CATEGORY_LABEL, 
            **common_settings, 
            ticktext=(df.loc[cat_x].TICKS_MIN, 
                      *blank_ticks, 
                      df.loc[cat_x].TICKS_MAX), 
        ),
        yaxis=dict(
            title=df.loc[cat_y].CATEGORY_LABEL, 
            **common_settings, 
            ticktext=(df.loc[cat_y].TICKS_MIN, 
                      *blank_ticks, 
                      df.loc[cat_y].TICKS_MAX), 
        ),
    )

    return fig


def radar_chart(pins):
    df = read_csv('data/skill_level.csv')

    categories = df.CATEGORY.unique()
    types = [k for k, v in pins.items() if v]

    fig = go.Figure()
    for t in types:
        fig.add_scatterpolar(
            r=df[df.TYPE == t].LEVEL.values, 
            theta=categories, 
            fill='toself', 
            name=t, 
        )
    fig.update_layout(
        height=600, 
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5], 
        )), 
        legend=dict(
            x=0.1, 
            y=-0.1, 
            xanchor='left', 
            yanchor='top', 
            orientation='h', 
        ), 
        showlegend=len(types)!=1
    )

    return fig
