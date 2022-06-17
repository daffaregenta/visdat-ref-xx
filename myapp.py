# Anggota Kelompok 

# - M Alif Naufal Yasin 1301184321
# - Novita 1301184101
# - M Aqmal Pangestu 1301180518


import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import widgetbox, row
from bokeh.models import Select
from bokeh.models import DateRangeSlider
import datetime as dt
from bokeh.models.widgets import Tabs, Panel

# Read dataset
df = pd.read_csv("./country_vaccinations.csv")

# Rename column for figure title support
col = {
    "total_vaccinations":"Total_Vaccine",
    "daily_vaccinations":"Daily_Vaccinations"
}
df.rename(col, axis=1, inplace=True)

df["Date"] = pd.to_datetime(df["date"]).dt.date
country_names = df['country'].value_counts().sort_index().index.tolist()

# Replace null/NaN values
df.fillna(0)

# Data sources
source_total_vaccine = ColumnDataSource(data={
    'Date' : df[df['country'] == 'Indonesia']['date'],
    'Total_Vaccine' : df[df['country'] == 'Indonesia']['Total_Vaccine']
})
source_daily_vaccination = ColumnDataSource(data={
    'Date' : df[df['country'] == 'Indonesia']['date'],
    'Daily_Vaccinations' : df[df['country'] == 'Indonesia']['Daily_Vaccinations']
})

# Tooltip
tooltip_total_vaccine = [
        ('Date', '@Date{%F}'),
        ('Total Vaccine', '@Total_Vaccine')
]
tooltip_daily_vaccination = [
        ('Date', '@Date{%F}'),
        ('Daily Vaccinations', '@Daily_Vaccinations')
]

fig_data_total_vaccine = figure(x_axis_type='datetime',
        plot_height=750, plot_width=1000,
        title='Country Total Vaccinations',
        x_axis_label='Date', y_axis_label='Total Vaccinations')
fig_data_daily_vaccination = figure(x_axis_type='datetime',
        plot_height=750, plot_width=1000,
        title='Country Daily Vaccinations',
        x_axis_label='Date', y_axis_label='Daily Vaccinations')


fig_data_total_vaccine.add_tools(HoverTool(tooltips = tooltip_total_vaccine, formatters={'@Date':'datetime'}))
fig_data_daily_vaccination.add_tools(HoverTool(tooltips = tooltip_daily_vaccination, formatters={'@Date':'datetime'}))


fig_data_total_vaccine.line('Date', 'Total_Vaccine',
                color='#CE1141',
                source=source_total_vaccine)
fig_data_daily_vaccination.line('Date', 'Daily_Vaccinations',
                color='#CE1141',
                source=source_daily_vaccination)

def update_data_total_vaccine(attr,old,new):
    [start, end] = slider.value
    date_from = dt.datetime.fromtimestamp(start/1000.0).date()
    date_until = dt.datetime.fromtimestamp(end/1000.0).date()

    data_location = str(location_select.value)

    # New data
    loc_date = df[(df['Date'] >= date_from) & (df['Date'] <= date_until)]
    new_data = {
        'Date' : loc_date[loc_date['country'] == data_location]['Date'],
        'Total_Vaccine' : loc_date[loc_date['country'] == data_location]['Total_Vaccine'],
    }
    source_total_vaccine.data = new_data
    
def update_data_daily_vaccination(attr, old, new):
    [start, end] = slider2.value
    date_from = dt.datetime.fromtimestamp(start/1000.0).date()
    date_until = dt.datetime.fromtimestamp(end/1000.0).date()

    data_location = str(location_select2.value)

    #new data
    loc_date = df[(df['Date'] >= date_from) & (df['Date'] <= date_until)]
    new_data = {
        'Date' : loc_date[loc_date['country'] == data_location]['Date'],
        'Daily_Vaccinations' : loc_date[loc_date['country'] == data_location]['Daily_Vaccinations'],
    }
    source_daily_vaccination.data = new_data
    
location_select = Select(
    options=[str(x) for x in country_names],
    value = 'Indonesia',
    title = 'Country'
)
location_select2 = Select(
    options=[str(x) for x in country_names],
    value = 'Indonesia',
    title = 'Country'
)

location_select.on_change('value',update_data_total_vaccine)
location_select2.on_change('value',update_data_daily_vaccination)


init_value = (df['Date'].min(), df['Date'].max())

slider = DateRangeSlider(start = init_value[0], end = init_value[1], value=init_value)
slider2 = DateRangeSlider(start = init_value[0], end = init_value[1], value=init_value)

slider.on_change('value' ,update_data_total_vaccine) 
slider2.on_change('value' ,update_data_daily_vaccination)

layout = row(widgetbox(location_select, slider), fig_data_total_vaccine)
layout2 = row(widgetbox(location_select2, slider2), fig_data_daily_vaccination)


panel = Panel(child=layout, title='Country Total Vaccine')
panel2 = Panel(child=layout2, title='Country Daily Vaccinations')

tabs = Tabs(tabs=[panel2,panel])

curdoc().add_root(tabs)
