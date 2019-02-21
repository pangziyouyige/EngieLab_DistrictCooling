import pandas as pd
import numpy as np

from bokeh.io import output_file, show, curdoc
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter, Slider, CheckboxGroup, HoverTool, Div, Paragraph
from bokeh.plotting import figure
from bokeh.sampledata.unemployment1948 import data
from bokeh.transform import transform
from bokeh.models.glyphs import ImageURL
from bokeh.layouts import column, row, widgetbox

def input():
	length = int(inbox("Enter length"))
	width = int(inbox("Enter width"))

def get_dataset(length=20, width=20):
	df = pd.DataFrame(np.random.randint(0,100, size=(length, width)))
	df = pd.DataFrame(df.stack(), columns=["score"]).reset_index()
	df.columns = ["length", "width", "score"]
	df["length"] = df["length"]+1
	df["width"] = df["width"]+1
	df.length = df.length.astype(str)
	df.width = df.width.astype(str)

	return ColumnDataSource(data = df)




def make_plot(source):
	#colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
	# colors = ["#550b1d", "#933b41", "#cc7878", "#ddb7b1", "#dfccce", "#e2e2e2", "#c9d9d3", "#a5bab7", "#75968f"]
	# mapper = LinearColorMapper(palette=colors, low=0, high=100)

	plot = figure(plot_width=800, plot_height=800, title = "", x_range=[str(x) for x in list(range(1, 11))], y_range=[str(x) for x in list(range(1, 11))], toolbar_location=None)
	plot.title.align = "right"
	plot.title.text_font_size = "15px"
	colors = ["#550b1d", "#933b41", "#cc7878", "#ddb7b1", "#dfccce", "#e2e2e2", "#c9d9d3", "#a5bab7", "#75968f"]
	mapper = LinearColorMapper(palette=colors, low=0, high=100)
	color_bar = ColorBar(color_mapper=mapper, location=(0, 0), ticker=BasicTicker(desired_num_ticks=len(colors)), formatter=PrintfTickFormatter(format="%d"), scale_alpha=0.4)
	plot.add_layout(color_bar, 'left')
	plot.image_url(url=['shtest/static/images/sh1.jpg'], x=0, y=0, w=10, h=10, anchor="bottom_left")
	plot.xgrid.grid_line_color = None
	plot.ygrid.grid_line_color = None
	plot.axis.visible=False
	#plot.rect(x="length", y="width", width=1, height=1, source=source, line_color=None, fill_color=transform('score', mapper), alpha=0.4)

	return plot




def update_plot(attr, old, new):
	length = slider.value
	width = slider.value
	new_df = get_dataset(length, width)
	source.data.update(new_df.data)
	plot.x_range.factors = [str(x) for x in list(range(1, length+1))]
	plot.y_range.factors = [str(x) for x in list(range(1, width+1))]
	plot.image_url(url=['shtest/static/images/sh1.jpg'], x=0, y=0, w=length, h=length, anchor="bottom_left")
	
	colors = ["#550b1d", "#933b41", "#cc7878", "#ddb7b1", "#dfccce", "#e2e2e2", "#c9d9d3", "#a5bab7", "#75968f"]
	mapper = LinearColorMapper(palette=colors, low=0, high=100)
	plot.rect(x="length", y="width", width=1, height=1, source=source, line_color=None, fill_color=transform('score', mapper), alpha=0.4)


	hover = HoverTool(tooltips=[("Potential Score for District Cooling", "@score")])
	plot.add_tools(hover)

	p.text = "<h><b>The Shanghai city has been evaluated by %d blocks for tessllation</b></h>" % (length*width)
	#plot.title.text = "The Shanghai city has been evaluated by %d blocks for tessllation" % (length*width)


slider = Slider(title = "size", start=5, end =20, step=1, value= 10)

factors = ["FAR (Floor Area Ratio)", "Building Type Mix Diversity", "Weather-Cooling Degree Days", "Urban Cooling Density", "Electricy Tariff", "Population and Urban Compactness", "GDP per Capita", "Ratio of Street Surface to Building Area", "Vegetation Coverage", "Building Shading and Urban Context", "Roof Coloar and Albedo", "Building Materials", "Vehicles and Transportation", "Percentage of Water Body"]



checkbox = CheckboxGroup(labels = factors, active = [])
source = get_dataset()
plot = make_plot(source)
p = Div(text="""<h><b>The Shanghai city is now being evaluated by __ blocks for tessllation</b></h>""", width=600, height=15)
img = Div(text="""<img src="shtest/static/images/icon.png" alt="Engie Lab China" height="55" width="90">""", width = 90, height = 55)

slider.on_change("value", update_plot)
checkbox.on_change("active", update_plot)




div = Div(text="""<h><b>WHERE TO DO BUSINESS FOR DISTRICT COOLING? </b></h></br></br>DEMO Created by <b><a href="https://twitter.com/Samirak93">Engie Lab China</a></b> using urban data and artificial intelligence to automatically tessellate the districts of a city and estimate the boundaries and potentials for implementing district cooling.<br></br><br></br>""",
width=780, height=70)


div_help = Div(text="""<b><h>INSTRUCTIONS</b></h></br></br>1.Drag the slider to choose the size of each block for tessellation, and select the urban factors from checkbox that should be considered to estimate the potential of district cooling for each block.<br></br>
<img src="https://bokeh.pydata.org/en/latest/_images/PointDraw.png" alt="Point Draw Tool">
<br></br> 
2.Scores representing the estimated potentials of implementing district cooling are given to blocks, encoded with different colors. Hover the blocks to check the exact scores.<br></br>
<img src="shtest/static/images/sh1.jpg" alt="Reference Map" height="200" width="200">
""",
width=600, height=150)

layout=column(row(div, img), row(plot, column(p, widgetbox(slider, checkbox),column(div_help))))

#layout = row(plot, column(widgetbox(slider, checkbox)))

# show(layout)

curdoc().add_root(layout)