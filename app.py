import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import seaborn as sns

# Load the Iris dataset
df = sns.load_dataset('iris')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the app layout
app.layout = html.Div([
    html.H1("Interactive Iris Dashboard"),
    dcc.Graph(id="sepal-scatter-plot"),
    dcc.Graph(id="petal-length-bar-chart"),
])

# Callback for updating sepal scatter plot
@app.callback(
    Output("sepal-scatter-plot", "figure"),
    [Input("petal-length-bar-chart", "clickData")]
)
def update_sepal_scatter_plot(click_data):
    species = df['species'].unique()
    if click_data:
        species = [click_data['points'][0]['x']]
    filtered_data = df[df['species'].isin(species)]
    fig = px.scatter(filtered_data, x="sepal_length", y="sepal_width", color="species")
    fig.update_layout(title="Sepal Length vs Sepal Width by Iris Species")
    return fig

# Callback for updating petal length bar chart
@app.callback(
    Output("petal-length-bar-chart", "figure"),
    [Input("sepal-scatter-plot", "relayoutData")]
)
def update_petal_length_bar_chart(relayout_data):
    if relayout_data is None:
        filtered_data = df
    else:
        xaxis_range = relayout_data.get("xaxis.range", None)
        if xaxis_range:
            min_x, max_x = xaxis_range
            filtered_data = df[(df['sepal_length'] >= min_x) & (df['sepal_length'] <= max_x)]
        else:
            filtered_data = df
    avg_petal_length = filtered_data.groupby("species")["petal_length"].mean().reset_index()
    fig = px.bar(avg_petal_length, x="species", y="petal_length", title="Average Petal Length by Species")
    return fig

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
