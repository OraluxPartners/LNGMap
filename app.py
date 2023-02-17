from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd

import plotly.graph_objects as go

df = pd.read_csv('lng_terminals.csv')

# print(df)

app = Dash(__name__)


hovertemplate = "<b>%{customdata[0]}</b><br><br>" + \
                "Status: %{customdata[1]}<br>" + \
                "Owner: %{customdata[2]}<br>" + \
                "Capacity: %{customdata[3]}<br>"


fig = go.Figure(data=go.Scattergeo(
    lon=df['lng'],
    lat=df['lat'],
    customdata=df[['lng_terminal', 'status', 'owner', 'capacity']],

    hovertemplate=hovertemplate,
    mode='markers',
    # marker_color='blue',
))

fig.update_layout(
    geo_scope='usa',

    margin=dict(l=0, r=0, t=0, b=0)
)


app.layout = html.Div(children=[


    html.Div(
        id="banner",
        className="banner",
        children=[
            html.H6("LNG Terminals in USA"),
            html.Img(src=app.get_asset_url("logo.png")),
        ],


    ),
    html.Div(
        className="map-container",
        children=[
            html.Div(
                
                dcc.Graph(
                    id='example-map',
                    figure=fig,
                    style={
                        'width': '80%',
                        'height': 'auto',
                        'display': 'block',
                        'margin-top': '20px',
                        'margin-left': 'auto',
                        'margin-right': 'auto',
                        'min-margin': '20px'
                    }
                ),),
            html.Div(
                dash_table.DataTable(id='table',
                    style={
                        'width': '80%',
                        'height': 'auto',
                        'display': 'block',
                        'margin-top': '20px',
                        'margin-left': 'auto',
                        'margin-right': 'auto',
                        'min-margin': '20px'
                    })
            ),
        ]),
])


@app.callback(
    Output('table', 'data'),
    [Input('example-map', 'clickData')]
)
def update_output(clickData):
    print("you are in the callback function")
    if clickData is not None:
        print(clickData)
        return df.to_dict('records')
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=False)
