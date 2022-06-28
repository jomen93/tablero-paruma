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

# =============================================================================
# Read the data
# =============================================================================
data_path = "data.xlsx"
df = pd.read_excel(data_path, engine="openpyxl")
df = df.dropna(how="all", axis=1)
df = df.drop_duplicates(subset="DOLOR")
columns_show = ["ID", "FECHA", "DOLOR", "SATIF", "CATEG"]
# =============================================================================
# Definicion de los tabs
# =============================================================================



children_list = [
    html.Div(
        className="mat-card",
        style = {
            "display":"block",
            "margin":"15px"},
        children = [
            html.H1(children="Segmentación de Opinión")
            ]
        ),
    html.Div(
        className="mat-card",
        style = {
            "display":"block",
            "margin":"15px"},
        children=[
            html.H4(children="Base de datos"),
            html.P("Se tiene una selección de las columnas más representativas de la base de datos "),
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
            ]
        ),
            
    ]



app.layout = html.Div(children=children_list)


# =============================================================================
# Callbacks
# =============================================================================
@app.callback(Output("tbl_out", "children"), Input("cust-table2", "active_cell"))
def cell_clicked(active_cell):
    return df.iloc[active_cell["row"]][active_cell["column_id"]] if active_cell else "Click the table"

if __name__ == "__main__":
    app.run_server(
        debug = True,
        host = "0.0.0.0",
        port = os.getenv("PORT", 8500),
        dev_tools_hot_reload=True
        )


