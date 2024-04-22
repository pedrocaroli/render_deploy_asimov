import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
 
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

load_figure_template("minty")

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
server = app.server

df = pd.read_excel('assets/BaseFuncionarios.xlsx')
df["Data de Contratacao"] = pd.to_datetime(df["Data de Contratacao"])
df

#fig = px.bar(df,x='Área', y = 'Salario Base')


#==================================================================================================================================
#Layout

app.layout = html.Div(id='div1',
    children=[
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H2("Primeiro Dash - PY BI"),
                    html.Hr(),
                    html.H5("Sexo"),
                    dcc.Checklist(df.Sexo.value_counts().index,df.Sexo.value_counts().index,
                    id= "sexo",inputStyle={"margin-right": "5px", "margin-left": "20px"}),

                    html.H5("Variável de análise:", style={"margin-top": "30px"}),
                    dcc.RadioItems(["Salario Base", "Impostos"], "Salario Base", id="variavel",
                    inputStyle={"margin-right": "5px", "margin-left": "20px"})
                ], style={"height": "90vh", "margin": "20px", "padding": "20px"})
            ],sm=2),

            dbc.Col([
                dcc.Graph(id="grafico_area")
            ],sm=10)
        ])
    ]                                           
)


# if __name__ == '__main__':
#     app.run_server(debug=True)

#------CALLBACKS-----------------------------------------------------------------------------------------
@app.callback(
            Output("grafico_area","figure"),
            [
                Input("sexo", "value"),
                Input("variavel","value")
            ])

def render_graphs(sexo,variavel):
    operacao = np.mean
    # variavel = "Impostos"
    df_filter = df[df["Sexo"].isin(sexo)]
    #df_filter.groupby("Área")[variavel].apply(operacao).to_frame().reset_index()
    df_sexo = df_filter.groupby("Área")[variavel].apply(operacao).to_frame().reset_index()

    fig = px.bar(df_sexo, x="Área", y=variavel)
    #fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template="minty")

    return fig  

# =========  Run server  =========== #
if __name__ == "__main__":
    app.run_server(debug=False)