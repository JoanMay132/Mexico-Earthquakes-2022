# Requirements
# 1. Upload a csv file with the data
# 2. Upload a GeoJSON file with the coordinates of the states

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash 
import numpy as np
import plotly.graph_objects as go


# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Earthquakes in Mexico"
server = app.server


# Scatter magnitudes
def scatter_magnitudes(df):

    fig=px.scatter_mapbox(df, 
        lat="Latitud", lon="Longitud", color="Magnitud", size="Magnitud", zoom=3.5, #height=500,
        )

    # update layout
    fig.update_layout(  mapbox_style="open-street-map",
                        margin={"r":0,"t":0,"l":0,"b":0}
                        ,
                        #width=600,
                        #height=500,
                        paper_bgcolor='white')
    return fig

"""
Este programa crea una gráfica de puntos, la cual es ideal para
mostrar la distribución completa de una muestra.

Los datos más nuevos se pueden obtener del siguiente enlace:

http://www2.ssn.unam.mx:8080/catalogo/

"""
# Este diccionario será utilizado para nuestras
# etiquetas del eje horizontal.
MESES = {
    1: "Ene.",
    2: "Feb.",
    3: "Mar.",
    4: "Abr.",
    5: "May.",
    6: "Jun.",
    7: "Jul.",
    8: "Ago.",
    9: "Sep.",
    10: "Oct.",
    11: "Nov.",
    12: "Dic."
}

  # Read the data.
df = pd.read_csv(r'Magnitudes_sismos_completos_2022.csv', parse_dates=["Fecha"],infer_datetime_format=True)
df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y-%m-%d %H:%M:%S")
print(df)
def main(df):

 # Creamos 12 tonos de colores tipo hsla, con 100% de saturación
    # 75% de iluminación y 90% de transparencia.    
    tonos_de_color = [
        f"hsl({h}, 100%, 75%, 0.9)" for h in np.linspace(0, 360, 12)]

    # Filtramos todos los sismos sin magnitud.
    df = df[df["Magnitud"] != "no calculable"].copy()

    # Convertimos las magnitudes a float.
    df["Magnitud"] = df["Magnitud"].astype(float)

    # Seleccionamos sismos de magnitud 6.0 o superior.
    df = df[df["Magnitud"] >= 0.3]

    fig2 = go.Figure()


    # Vamor a iterar sobre todos los meses y extraer los sismos correspondientes.
    for numero, mes in MESES.items():

        # Seleccionamos todos los sismos del mes correspondiente.
        temp_df = df[df["Fecha"].dt.month == numero]

        # Vamos a crear la etiqueta para el eje horizontal.
        # Esta etiqueta es la misma cadena de caracteres repetida el 'numero
        # de veces igual al largo del DataFrame del mes correspondiente.
        etiquetas = [f"{mes} ({len(temp_df)})" for _ in range(len(temp_df))]
        
        # Las magnitudes son extraídas de la columna y convertidas a una lista.
        magnitudes = temp_df["Magnitud"].tolist()

        # Para crear una gráfica de puntos debemos modificar una de tipo Box.
        # Lo que hacemos es mostrar todos los puntitos, hacer invisibles los bigotes
        # y las cajas.
        # Los dos parámetros más importantes boxpoints y pointpos, los cuales
        # nos permiten mostrar todos los puntos y centrarlos donde iban las cajas.
        # Al final seleccionamos el tono de color correspondiente al mes.
        fig2.add_traces(
            go.Box(
                
                x=etiquetas,
                y=magnitudes,
                boxpoints="all",
                pointpos=0,
                whiskerwidth=0,
                line_width=0,
                fillcolor="hsla(0, 0, 0, 0)",
                jitter=1,
                marker_size=12,
                marker_color=tonos_de_color[-numero]
                
            )
            

        )

    fig2.update_xaxes(
        title="Month of occurrence (Total records)",
        ticks="outside",
        ticklen=10,
        tickfont_size=14,
        title_standoff=18,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.0,
        showline=True,
        mirror=True
    )

    fig2.update_yaxes(
        title="Earthquake Magnitude",
        range=[0.3, 8.4],
        ticks="outside",
        tickfont_size=14,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=20
    )

    fig2.update_layout(
        showlegend=False,
        width=980,
        height=720,
        font_family="Quicksand",
        font_color="white",
        font_size=18,
        
        title_x=0.5,
        title_y=0.965,
        margin_t=60,
        margin_l=100,
        margin_r=40,
        margin_b=90,
        title_font_size=24,
        plot_bgcolor="#20252f",
        paper_bgcolor="#1E1E1E",
        annotations=[
            dict(
                x=-0.1,
                y=-0.17,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Source: SSN"
            ),
            dict(
                x=1.01,
                y= -0.19,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🦦 @JoanMay132"
            )
        ])
    return fig2
# Create the app
app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                # html.A(
                #     html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                #     href="https://plotly.com/dash/",
                # ),
                html.A(
                    html.Button("Linkedln", id="link-button"),
                    href="https://www.linkedin.com/in/joanmay132/",
                ),
                html.A(
                    html.Button("Source Code", className="link-button"),
                    href="https://github.com/JoanMay132/Mexico-Earthquales-2022.git",
                ),
                html.H4(children="Earthquakes in Mexico 2022"),
                html.P(
                    id="description",
                    children="† Mexico City is no stranger to earthquakes. In fact, the country trembles almost every day.\
                                This is because the west coast of Mexico is located along the so-called “Ring of Fire:” a \
                                horseshoe shape that curves around the edges of the Pacific Ocean. All the way from Australia \
                                to the Andes, it’s where 90 percent of the world’s seismic activity takes place. \
                                When visiting or living in Mexico City it is important to be aware of the risk of a possible earthquake \
                                and be prepared on how to act and protect yourself and others.                    "),
        ],
       
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                dcc.RangeSlider(
                                    id="years-slider",
                                    min=df['Magnitud'].min(),
                                    max=df['Magnitud'].max(),
                                    step=0.6,
                                    value=[3,4],
                                    tooltip={'placement': 'bottom','always_visible': True}
                                    

                                ),
                            ],
                        ),
                         html.Div(
                        id="heatmap-container",
                        children=[
                            html.P(
                                "Magnitude map of all earthquakes in Mexico in 2022",
                                id="heatmap-title"),
                            dcc.Graph(
                                id="county-choropleth",
                                figure=scatter_magnitudes(df),
                               
                            ),
                        
                        ],
                    ),
               
                    ]
                    
                )
            ],
        ),

        html.Div(
            id="graph-container",
            children=[
                html.P(id="chart-selector", children="Data Table of all earthquakes in Mexico in 2022"),
                dash_table.DataTable(
                    
                    id='tablesitas',            
                    
                    
                    columns=[
                        {"name":"Fecha UTC", "id":"Fecha UTC"},
                        {"name":"Hora UTC", "id":"Hora UTC"},
                         {"name":"Magnitud", "id":"Magnitud"},
                        {"name":"Latitud", "id":"Latitud"},
                        {"name":"Longitud", "id":"Longitud"},
                       
                        {"name":"Profundidad", "id":"Profundidad"},
                        {"name":"Referencia de localizacion", "id":"Referencia de localizacion"},
                        {"name":"Estatus", "id":"Estatus"},

                        
                    ],

                    data=df.to_dict('records'),
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#d9ecd0'
                        },
                    ],

                    ),
            ],
        ),
        html.Div(
             id="puntos-container",
             children=[
                 html.P(id="chart-seleccion", children="Distribution of earthquakes by month of occurrence in Mexico (2022)"),
                 dcc.Graph(
                     id="puntos",
                     figure=main(df),
                     ),
             ],
        ),
        html.Div(
            id="footer",
            children=[
                html.P(
                    "This app was created by Joan May. The data was obtained from the National Seismological Service (SSN) of Mexico. The code is available on GitHub.",
                    id="footer-credits",
                ),
                html.A(
                    html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                    href="https://plotly.com/",
                ),


            ],


        ),

    ]
)
                

   

@callback(
    Output('county-choropleth', 'figure'),
    Input('years-slider', 'value')
)


def update_graph(Magnitude_list):
    dff = df[(df['Magnitud'] >= Magnitude_list[0]) & (df['Magnitud'] <= Magnitude_list[1])]
    print(dff.head())
    fig=px.scatter_mapbox(dff,
                    lat='Latitud',
                    lon='Longitud',
                    size='Magnitud',
                    color='Magnitud',
                    color_continuous_scale=px.colors.sequential.Rainbow,
                    size_max=15,
                    zoom=3.5,
                    
                    
                    )
    
    fig.update_layout(  mapbox_style="open-street-map",
                        margin={"r":0,"t":0,"l":0,"b":0},
                        paper_bgcolor='white')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)