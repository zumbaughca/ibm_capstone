import pandas as pd 
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()

def filter_payload_range(df, min_val, max_val):
    return df[(df['Payload Mass (kg)'] > min_val) & (df['Payload Mass (kg)'] < max_val)]

app = dash.Dash(__name__)

app.layout = html.Div(children = [
    html.H1('SpaceX Launch Records Dashboard',
            style = {'textAlign': 'center',
                     'color': '#503D36',
                     'font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': "All Sites", 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
        value = 'ALL',
        placeholder = "Select a location...",
        searchable = True
        ),
    
    dcc.Graph(id='success-pie-chart'),
    
    dcc.RangeSlider(id='payload-slider',
                    min = 0, max=10000, step=100,
                    marks = {0: '0',
                             2500: '2500',
                             5000: '5000',
                             7500: '7500',
                             10000: '10000'},
                    value = [min_payload, max_payload]),
    dcc.Graph(id='success-payload-scatter')
    ])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
    )
def get_pie_chart(site):
    filtered_df = df[df['Mission Outcome'] == 'Success']
    if site == 'ALL':
        fig = px.pie(df, 
                     names=df['Launch Site'],
                     values=df['class'],
                     title = 'All Sites')
        return fig
    else:
        site_df = df[df['Launch Site'] == site]
        fig = px.pie(site_df,
                     names=site_df['class'],
                     title = site)
        return fig
    
@app.callback(
    Output(component_id='success-payload-scatter', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
    )
def get_payload_scatter(site, payload_range):
    if site == 'ALL':
        filtered_df = filter_payload_range(df, payload_range[0], payload_range[1])
        fig = px.scatter(filtered_df, 
                         x = 'Payload Mass (kg)',
                         y = 'class',
                         color = 'Booster Version Category',
                         title = "Correlation between Payload and Success for all sites")
        return fig
    else:
        site_df = df[df['Launch Site'] == site]
        filtered_df = filter_payload_range(site_df, payload_range[0], payload_range[1])
        print(filtered_df.head())
        fig = px.scatter(filtered_df,
                         x = 'Payload Mass (kg)',
                         y = 'class',
                         color = 'Booster Version Category',
                         title = "Correlation between payload and success for {}".format(site))
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)