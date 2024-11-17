import plotly.graph_objects as go
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from pymongo import MongoClient
import datetime

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['data_db']

def insert_default_keys(collection, data, default_keys):
    for item in data:
        for key in default_keys:
            item.setdefault(key, None)
    collection.insert_many(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Save the data to MongoDB
        data = {col: request.form[col] for col in request.form}
        data['timestamp'] = datetime.datetime.now()
        db.scatter_data.insert_one(data)

        # Process scatter plot data
        x_values = request.form['x'].split(',')
        y_values = request.form['y'].split(',')
        scatter_data = {
            'x': [float(val) for val in x_values],
            'y': [float(val) for val in y_values]
        }
        db.scatter_data.insert_one(scatter_data)

        return redirect(url_for('index'))

    return render_template('form.html')

# ...

# ...

@app.route('/linegraph')
def line_graph():
    # Fetch data from MongoDB for line graph
    data = db.scatter_data.find_one({}, {'_id': 0}, sort=[('timestamp', -1)])

    # Convert 'x' and 'y' values from strings to arrays
    x_values = [float(val) for val in data['x'].split(',')]
    y_values = [float(val) for val in data['y'].split(',')]

    # Create a line graph using Plotly
    fig = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='lines'))
    line_graph_html = fig.to_html(full_html=False)

    return render_template('line_graph.html', line_graph_html=line_graph_html)

@app.route('/scatterplot')
def scatter_plot():
    # Fetch data from MongoDB for scatter plot
    data = db.scatter_data.find_one({}, {'_id': 0}, sort=[('timestamp', -1)])

    # Convert 'x' and 'y' values from strings to arrays
    x_values = [float(val) for val in data['x'].split(',')]
    y_values = [float(val) for val in data['y'].split(',')]

    # Create a scatter plot using Plotly
    fig = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='markers'))
    scatter_plot_html = fig.to_html(full_html=False)

    return render_template('scatter_plot.html', scatter_plot_html=scatter_plot_html)

# ... (existing code)

@app.route('/barchart')
def bar_chart():
    # Fetch data from MongoDB for bar chart
    data = db.scatter_data.find_one({}, {'_id': 0}, sort=[('timestamp', -1)])

    # Convert 'x' and 'y' values from strings to arrays
    x_values = [float(val) for val in data['x'].split(',')]
    y_values = [float(val) for val in data['y'].split(',')]

    # Create a bar chart using Plotly
    fig = go.Figure(data=go.Bar(x=x_values, y=y_values))
    bar_chart_html = fig.to_html(full_html=False)

    return render_template('bar_chart.html', bar_chart_html=bar_chart_html)

# ... (existing code)

@app.route('/piechart')
def pie_chart():
    # Fetch data from MongoDB for pie chart
    data = db.scatter_data.find_one({}, {'_id': 0}, sort=[('timestamp', -1)])

    # Convert 'x' and 'y' values from strings to arrays
    x_values = [str(val) for val in data['x'].split(',')]
    y_values = [float(val) for val in data['y'].split(',')]

    # Create a pie chart using Plotly
    fig = go.Figure(data=go.Pie(labels=x_values, values=y_values))
    pie_chart_html = fig.to_html(full_html=False)

    return render_template('pie_chart.html', pie_chart_html=pie_chart_html)

# ... (remaining code)

if __name__ == '__main__':
    app.run(debug=True)
