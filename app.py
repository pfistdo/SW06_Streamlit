import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from math import ceil

st.set_page_config(page_title="World Happiness Report")

# Write header
st.title('World Happiness Report')
st.write('''The World Happiness Report is a publication of the Sustainable Development Solutions Network, 
powered by the Gallup World Poll data. The World Happiness Report reflects a worldwide demand for more 
attention to happiness and well-being as criteria for government policy. It reviews the state of happiness 
in the world today and shows how the science of happiness explains personal and national variations in happiness.''')

# read happiness report and column descriptions
full_report = pd.read_csv("data/World_Happiness_Report.csv")
column_descriptions = pd.read_csv("data/column_descs.csv", names=['column', 'description'], sep=';')
with st.expander("View full happiness report"):
    st.write(full_report)


### SIDE BAR ###
st.sidebar.header('Filter options')
selected_year = st.sidebar.selectbox(
    'Year', np.sort(full_report['Year'].unique()), help="Select a year to generate a report", index=16)
selected_country = st.sidebar.selectbox('Country', full_report['Country Name'].unique(),
                                        help="Select a country to generate a report", index=142)
selected_compare_countries = st.sidebar.multiselect(
    'Compare selected with these countries',
    full_report['Country Name'].unique(),
    ['United States', 'Germany', 'Japan'],
    help="Select countries to compare with selected country")


### PROCESS DATA ###
# # Generate new dataframe for selected year
st.header(f"Report for {selected_country} of {selected_year}")
past_years = full_report[(full_report['Country Name'].isin([selected_country] + selected_compare_countries)) & (
    full_report['Year'] <= selected_year)]
st.write(past_years[(past_years['Year'] == selected_year) &
         (past_years['Country Name'] == selected_country)])

# Create new dataframe based on selected countries for only current and past years
with st.expander("View report of past years"):
    st.write(past_years[(past_years['Year'] <= selected_year) &
         (past_years['Country Name'] == selected_country)])
    
#>>> Generate metrics for selected year
st.subheader("Metrics for selected year compared to previous year")
col1, col2, col3, col4 = st.columns(4)
for index, col in enumerate(column_descriptions['column']):
  # TODO: Check ifprevious year exists
  value_selected_year = past_years[(past_years['Year'] == selected_year) & (past_years['Country Name'] == selected_country)][col].values[0]
  value_previous_year = past_years[(past_years['Year'] == selected_year-1) & (past_years['Country Name'] == selected_country)][col].values[0]
  delta = ceil((value_selected_year - value_previous_year)*100)/100
  value_selected_year = ceil(value_selected_year*100)/100
  if index % 4 == 0:
    col1.metric(label=col, value=value_selected_year, delta=delta)
  elif index % 4 == 1:
    col2.metric(label=col, value=value_selected_year, delta=delta)
  elif index % 4 == 2:
    col3.metric(label=col, value=value_selected_year, delta=delta)
  else:
    col4.metric(label=col, value=value_selected_year, delta=delta)

#>>> Generate line chart for past years
st.subheader("Line charts for past years")
selected_column = st.selectbox('Column', column_descriptions['column'], help="Select a column to generate a line chart")
# Get column description
column_description = column_descriptions[column_descriptions['column'] == selected_column]['description'].values[0]
st.caption(column_description)
# Generate line chart
line_chart = alt.Chart(past_years).mark_line(point=True).encode(
    x='Year:N',
    y=alt.Y(selected_column, type='quantitative', scale=alt.Scale(zero=False)),
    tooltip=[selected_column, 'Year'],
      color='Country Name')
st.altair_chart(line_chart, use_container_width=True)