import requests
from bs4 import BeautifulSoup
import pandas as pd
import dash
from dash import html, dash_table
from dash.dependencies import Input, Output

# getting data from provided url and finding direct link to csv
def fetch_data_from_url():
    response = requests.get("https://gist.github.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19")
    response.raise_for_status()  # raise an exception for HTTP errors
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        if link.get('href').endswith('.csv'):
            return "https://gist.githubusercontent.com" + link.get('href').replace("/raw/", "/raw/bd584ee6c307cc9fab5ba38916e98a85de9c2ba7/")


#removing extra columns which are not necesarry for us

def clean_csv_content(raw_data):
    lines = [line.split(',') for line in raw_data.splitlines()]
    headers = lines[0]
    num_columns = len(headers)
    filtered_lines = [line[:num_columns] for line in lines]
    return "\n".join([",".join(line) for line in filtered_lines])

def save_filtered_csv_to_file(csv_content):
    with open("pokemon.csv", "w") as f:
        f.write(csv_content)
    print("CSV saved to pokemon.csv")


def fetch_and_save_pokemon_data():
    raw_link = fetch_data_from_url()
    response = requests.get(raw_link)
    response.raise_for_status()
    cleaned_csv_content = clean_csv_content(response.text)
    save_filtered_csv_to_file(cleaned_csv_content)



fetch_and_save_pokemon_data()

# Initialize Dash app
app = dash.Dash(__name__)

@app.callback(
    Output('table', 'data'),
    [Input('refresh-button', 'n_clicks')]
)
def update_table(n):
    # This will re-fetch and save the pokemon data every time the button is clicked
    fetch_and_save_pokemon_data()
    df = pd.read_csv("pokemon.csv")
    return df.to_dict('records')

app.layout = html.Div([
    html.H1("Pokemon Data"),
    html.Button('Refresh Data', id='refresh-button', n_clicks=0),
    dash_table.DataTable(
        id='table',
        columns=[
            {"name": i, "id": i} for i in pd.read_csv("pokemon.csv").columns
        ],
        data=pd.read_csv("pokemon.csv").to_dict('records')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)