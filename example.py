import dash
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dash_table.DataTable(id='table'),
    html.Button('Update', id='button'),
])

# Define the initial data for the table
data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

# Define the callback to update the table when the button is clicked
@app.callback(Output('table', 'data'),
              [Input('button', 'n_clicks')],
              [State('table', 'data')])
def update_table(n_clicks, rows):
    if n_clicks is None:
        # Return the initial data
        return data.to_dict('records')
    else:
        # Modify the data based on user input
        # and return the updated data
        rows.append({'x': 4, 'y': 7})
        return rows

if __name__ == '__main__':
    app.run_server(debug=True)
