"""
Bokeh provides an interactive way of visualising data. This a good way to visualise products with similar ingredients. With Bokeh the closer the products are, the more similar ingredients they have and it also shows the ranking, the price and the brand of all products.
"""

# import libraries
from bokeh.io import show, curdoc, output_notebook, push_notebook
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select, Paragraph, TextInput
from bokeh.layouts import widgetbox, column, row
from ipywidgets import interact
import pandas as pd

df_bokeh = pd.read_csv("Data/cosmetic_TSNE.csv")

"""
This is for Bokeh to create all possible combinations based on the options from category of products and skin type
"""
# cosmetic filtering options 
option_1 = ['Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye cream', 'Sun protect']
option_2 = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']


output_notebook() # plot will be shown inside the notebook

""" Creating plot, glyphs and adding hover tool"""

# make a source and scatter bokeh plot  
source = ColumnDataSource(df_bokeh)
plot = figure(x_axis_label = 'T-SNE 1', y_axis_label = 'T-SNE 2', 
              width = 500, height = 400)
plot.circle(x = 'X', y = 'Y', source = source, 
            size = 10, color = '#FF7373', alpha = .8)

plot.background_fill_color = "beige"
plot.background_fill_alpha = 0.2

# add hover tool
hover = HoverTool(tooltips = [
        ('Item', '@name'),
        ('brand', '@brand'),
        ('Price', '$ @price'),
        ('Rank', '@rank')])
plot.add_tools(hover)


def update(select1 = option_1[0], select2 = option_2[0]):
    """Callback to update the plot"""
    
    a_b = select1 + '_' + select2
    new_data = {
        'X' : df_bokeh[df_bokeh['Label'] == a_b]['X'],
        'Y' : df_bokeh[df_bokeh['Label'] == a_b]['Y'],
        'name' : df_bokeh[df_bokeh['Label'] == a_b]['name'],
        'brand' : df_bokeh[df_bokeh['Label'] == a_b]['brand'],
        'price' : df_bokeh[df_bokeh['Label'] == a_b]['price'],
        'rank' : df_bokeh[df_bokeh['Label'] == a_b]['rank'],
    }
    source.data = new_data
    push_notebook()

# Plot with callback and interaction
interact(update, select1 = option_1, select2 = option_2)
show(plot, notebook_handle = True)