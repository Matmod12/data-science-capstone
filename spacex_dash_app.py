# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[
                                    {'label':'All Sites', 'value':'ALL'},
                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}
                                ], value='ALL', placeholder='Select a launch site here',
                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000,
                                step=1000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), 
              Input(component_id='site-dropdown', component_property='value'))
def succes_pie_chart(site):
    if site=='ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', 
        title='Successful launches of all launch sites')
    else:
        site_success = spacex_df[spacex_df['Launch Site']==site]
        fig = px.pie(site_success, names='class', color='class',
        color_discrete_map={1:'red', 0:'blue'},
        title=f'Successful launches for {site} launch site',
        labels={1:'Success', 0:'Failure'})
        fig.for_each_trace(lambda t: t.update( 
        labels=[{1:'Success', 0:'Failure'}[label] for label in t.labels]))

    fig.update_layout(legend=dict(yanchor="top", y=0.9,
                          xanchor="left", x=0.6),
                      title=dict(yanchor='top', y=0.9,
                          xanchor='left', x=0.4))
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', 
                     component_property='figure'), 
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')] )
def success_scatter(site, payload_range):
    payload_range[0] = payload_range[0]-100
    payload_range[1] = payload_range[1]+100
    if site=='ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category',
        title='Payload vs success for all sites')
    else:
        site_df = spacex_df[spacex_df['Launch Site']==site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title=f'Payload vs success for {site} launch site')

    fig['layout'].update(xaxis=dict(range=payload_range))
    fig.update_layout(legend=dict(yanchor="top", y=0.8,
                          xanchor="left", x=0.01),
                      title=dict(yanchor='top', y=0.9,
                          xanchor='left', x=0.4))
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
