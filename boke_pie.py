from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template, jsonify, request
from bokeh.models.sources import AjaxDataSource
from math import pi

import pandas as pd

from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.transform import cumsum

from random import randint

app = Flask(__name__)

@app.route('/data/', methods=['POST'])
def data():
    x = { 'United States': 143, 'United Kingdom': 10, 'Japan': randint(0,150), 'China': randint(0,150),
        'Germany': 76, 'India': 89, 'Italy': 67, 'Australia': 47,
        'Brazil': 12, 'France': 45, 'Taiwan': 42, 'Spain': 16 }

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(x)]    
    return jsonify(angle=list(data['angle']),country=list(data['country']),value=list(data['value']),color=list(data['color']))


@app.route('/dashboard/')
def show_dashboard():
    plots = []
    plots.append(make_ajax_plot())
    return render_template('dashboard.html', plots=plots)

def make_ajax_plot():
    test = AjaxDataSource(data_url=request.url_root + 'data/',
                            polling_interval=2000, mode='replace')

    test.data = dict(angle=[],country=[],value=[],color=[])

    print(test.data)
    
    plot = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
        tools="hover", tooltips="@country: @value")

    plot.annular_wedge(x=0, y=1, inner_radius=0.2, outer_radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color=None, fill_color='color', legend='country', source=test)

    plot.axis.axis_label=None
    plot.axis.visible=False
    plot.grid.grid_line_color = None


    script, div = components(plot)
    return script, div

if __name__== '__main__':
    app.run(host='localhost', port=8008, debug=True)
