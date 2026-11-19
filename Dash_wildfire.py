
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Create the Dash application
app = dash.Dash(__name__)

# Load the wildfire dataset
df = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/'
    'Data%20Files/Historical_Wildfires.csv'
)

# Extract month and year from the date
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Check that the dataset loaded correctly
print(df.head())


# Task 2.1: Dashboard title
# Task 2.2: Region radio buttons and year dropdown
# Task 2.3: Two chart containers

app.layout = html.Div(children=[

    html.H1(
        'Australia Wildfire Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 26
        }
    ),

    # Region selection
    html.Div([
        html.H2(
            'Select Region:',
            style={'margin-right': '2em'}
        ),

        dcc.RadioItems(
            options=[
                {'label': 'New South Wales', 'value': 'NSW'},
                {'label': 'Northern Territory', 'value': 'NT'},
                {'label': 'Queensland', 'value': 'QL'},
                {'label': 'South Australia', 'value': 'SA'},
                {'label': 'Tasmania', 'value': 'TA'},
                {'label': 'Victoria', 'value': 'VI'},
                {'label': 'Western Australia', 'value': 'WA'}
            ],
            value='NSW',
            id='region',
            inline=True
        )
    ]),

    # Year selection
    html.Div([
        html.H2(
            'Select Year:',
            style={'margin-right': '2em'}
        ),

        dcc.Dropdown(
            options=sorted(df['Year'].unique().tolist()),
            value=2005,
            id='year'
        )
    ]),

    # Task 2.3: Chart containers
    html.Div([

        html.Div(
            [],
            id='plot1',
            style={'width': '50%'}
        ),

        html.Div(
            [],
            id='plot2',
            style={'width': '50%'}
        )

    ], style={'display': 'flex'})

])


# Task 2.4: Connect inputs and outputs
@app.callback(
    [
        Output('plot1', 'children'),
        Output('plot2', 'children')
    ],
    [
        Input('region', 'value'),
        Input('year', 'value')
    ]
)

# Task 2.5: Create interactive charts
def reg_year_display(input_region, input_year):

    # Filter data by selected region
    region_data = df[df['Region'] == input_region]

    # Filter data by selected year
    y_r_data = region_data[
        region_data['Year'] == input_year
    ]

    # Chart 1: Monthly average estimated fire area
    est_data = (
        y_r_data.groupby('Month')['Estimated_fire_area']
        .mean()
        .reset_index()
    )

    fig1 = px.pie(
        est_data,
        values='Estimated_fire_area',
        names='Month',
        title=(
            f'{input_region} : Monthly Average '
            f'Estimated Fire Area in year {input_year}'
        )
    )

    # Chart 2: Monthly average vegetation fire pixel count
    veg_data = (
        y_r_data.groupby('Month')['Count']
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        veg_data,
        x='Month',
        y='Count',
        title=(
            f'{input_region} : Average Count of Pixels '
            f'for Presumed Vegetation Fires in year {input_year}'
        )
    )

    # Return both charts to the dashboard
    return [
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2)
    ]


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
