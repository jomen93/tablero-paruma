#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Johan Mendez
"""

# =============================================================================
# librerias
# =============================================================================
from app import app
from dash import html, dcc, dash_table, no_update
import dash_bootstrap_components as dbc
import os
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


# =============================================================================
# Read the data
# =============================================================================
data_path = "data.xlsx"
df = pd.read_excel(data_path, engine="openpyxl")
len_original = df.shape[0]
df = df.dropna(how="all", axis=1)
val_dup = df.drop_duplicates(subset="DOLOR").shape[0]
df = df.drop_duplicates(subset="DOLOR")
columns_show = ["ID", "FECHA", "DOLOR", "SATIF", "CATEG"]
df = df.drop(df.index[2046], axis=0)
df = df.drop(df.index[4195], axis=0)

# Fechas para la tarjeta
df["FECHA"] = pd.to_datetime(df["FECHA"]).dt.date
date_min = str(pd.to_datetime(df["FECHA"].min()).date())
date_max = str(pd.to_datetime(df["FECHA"].max()).date())

# =============================================================================
# Definicion de los tabs
# =============================================================================
# Longitudes de las clases de los histogramas 
lengths = [len(df["DOLOR"].iloc[i]) for i in range(df["DOLOR"].shape[0])]

layout = go.Layout(plot_bgcolor="rgba(0,0,0,0)", title="¿Qué tan largas son las opiniones?")
fig = go.Figure(layout=layout)
fig.add_trace(
    go.Histogram(x=lengths))
fig.update_xaxes(
    title_text = "Número de palabras",
    minor=dict(ticklen=6, tickcolor="black"),
    showgrid=True,
    showline=True,
    gridcolor="#D6D6D6",
    linecolor="black",
    mirror=True)
fig.update_yaxes(
    title_text = "Frecuencia",
    minor_ticks="inside",
    tickcolor="black",
    showline=True,
    linecolor="black",
    gridcolor="#D6D6D6",
    mirror=True)

# valores para la segunda grafica de valores nulos 
nan_columns = df.columns[df.isnull().any()]
values_nan = df[nan_columns].isnull().mean().values
size_bin = abs(np.min(values_nan)-np.max(values_nan))/len(values_nan)
fig1 = go.Figure(layout=layout)
fig1.add_trace(
    go.Histogram(x=values_nan, 
        xbins=dict(start=0.0, end=1.0, size=0.007))
)

fig1.update_xaxes(
    title_text = "Número de palabras",
    minor=dict(ticklen=6, tickcolor="black"),
    showgrid=True,
    showline=True,
    gridcolor="#D6D6D6",
    linecolor="black",
    mirror=True)
fig1.update_yaxes(
    title_text = "Frecuencia",
    minor_ticks="inside",
    tickcolor="black",
    showline=True,
    linecolor="black",
    gridcolor="#D6D6D6",
    mirror=True)
#valores para la tercera grafica
fig2 = go.Figure(layout=layout)
fig2.add_trace(
    go.Box(y=lengths, boxpoints="outliers")
    )

fig2.update_xaxes(
    title_text = "Número de palabras",
    minor=dict(ticklen=6, tickcolor="black"),
    showgrid=True,
    showline=True,
    gridcolor="#D6D6D6",
    linecolor="black",
    mirror=True)
fig2.update_yaxes(
    title_text = "Frecuencia",
    minor_ticks="inside",
    tickcolor="black",
    showline=True,
    linecolor="black",
    gridcolor="#D6D6D6",
    mirror=True)

children_list = html.Div(children=[
    dbc.Row([
        dbc.Col(
            html.H1("Segmentación de opinión"), 
            className="mat-card",
            width=12,
            style={"margin":"5px"}
            ),
        ]),
    dbc.Row([
        dbc.Col([html.Div([
            html.H6("Longitud de los datos"),
            html.P(len_original)

            ])], 
            className="mat-card",
            width=3,
            ),
        dbc.Col([html.Div([
            html.H6("Datos duplicados"),
            html.P(len_original - val_dup)
            ])], 
            className="mat-card",
            width=3,
            ),
        dbc.Col([html.Div([
            html.H6("# Categorías"),
            html.P(len(df["CATEG"].unique()))
            ])], 
            className="mat-card",
            width=3,
            ),
        dbc.Col([html.Div([
            html.H6("Rango de fechas"),
            html.P(date_min +" | "+ date_max )
            ])], 
            className="mat-card",
            width=3,
            ),
        ]),

    dbc.Row([
        dbc.Col([
            html.H4("Base de datos"),
            html.P("Columnas más importantes de la base"),
            dash_table.DataTable(
                id = "cust-table2",
                data=df[columns_show].to_dict("records"),
                columns = [{"name":i, "id":i} for i in columns_show],
                style_header={"background":"white", "fontWeight":"bold"},
                style_table={"overFlowX":"auto"},
                style_cell={
                "fontFamily":"Open Sans",
                "textAlign":"center",
                "overflow":"hidden",
                "textOverflow":"ellipsis",
                "maxWidth":"180px"
                },
                page_size=11,
                page_current=0,
                page_action = "native"
                ),
            dbc.Alert(id="tbl_out")
            ],className="mat-card",
            width=12,
            style={"margin":"5px"}
            ),
        ]),
    dbc.Row([
        dbc.Col([html.Div([
            html.H4("Limpieza de datos"),
            dcc.Graph(id="plot1", figure=fig)
            ])], 
            className="mat-card",
            width=4,
            ),
        dbc.Col([html.Div([
            html.H4("Valores Perdidos"),
            dcc.Graph(id="plot2", figure=fig1)
            ])], 
            className="mat-card",
            width=4,
            ),
        dbc.Col([html.Div([
            html.H4("Datos atípicos en longitud"),
            dcc.Graph(id="plot3", figure=fig2)
            ])], 
            className="mat-card",
            width=4,
            ),
        ]),
    ])



app.layout = children_list


# =============================================================================
# Callbacks
# =============================================================================
@app.callback(Output("tbl_out", "children"), Input("cust-table2", "active_cell"))
def cell_clicked(active_cell):
    return df.iloc[active_cell["row"]][active_cell["column_id"]] if active_cell else "Consulte información con un click"



if __name__ == "__main__":
    app.run_server(
        debug = True,
        host = "0.0.0.0",
        port = os.getenv("PORT", 8500),
        dev_tools_hot_reload=True
        )



