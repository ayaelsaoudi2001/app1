import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_csv('C:/Users/acc/Desktop/spring 2024/MSBA325 - Data Visualization & Communication/assignment 1/jobs_in_data.csv')
data_science=data[data['job_category']=='Data Science and Research']

st.header('Visualization #1:')
st.subheader('visualizing the avarage salary of data scientists in each country')

average_salary_by_country = data_science.groupby('company_location')['salary_in_usd'].mean().reset_index()

fig1 = px.choropleth(
    data_frame=average_salary_by_country,
    locations='company_location',
    locationmode='country names',
    color='salary_in_usd',
    hover_name='company_location',
    custom_data=['company_location'],
    color_continuous_scale='Viridis',
    labels={'salary_in_usd': 'Average Salary (USD)'}
)

fig1.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Average Salary: $%{z:.2f}k')

st.plotly_chart(fig1)

countries = data_science['company_location'].unique().tolist()

st.header('Visualization #2:')
st.subheader('visualizing the avarage salary of data scientists in each country over the years')


# Create Subplots
fig2 = make_subplots(rows=1, cols=1, subplot_titles=['Average Salary Trends Over Years'])

for i, country in enumerate(countries):
    data_science_selected = data_science[data_science['company_location'] == country]
    average_salary_by_year = data_science_selected.groupby('work_year')['salary_in_usd'].mean().reset_index()
    trace = go.Scatter(
        x=average_salary_by_year['work_year'],
        y=average_salary_by_year['salary_in_usd'],
        mode='lines+markers',
        name=country
    )
    fig2.add_trace(trace)
    visibility = [loc == 'United States' for loc in countries]
    fig2.update_traces(visible=visibility, selector=f"legendonly{i + 1}")

# Update Layout
fig2.update_layout(
    updatemenus=[
        dict(
            type='dropdown',
            x=-0.06,
            y=1,
            showactive=True,
            active=countries.index('United States'),  # Set the active button
            buttons=[
                dict(
                    label=country,
                    method='update',
                    args=[
                        {'visible': [True if loc == country else False for loc in countries]},
                        {'title': f'Average Salary Trends in {country} Over Years'}
                    ]
                )
                for country in countries
            ],
        )
    ]
)

fig2.update_layout(title_text='Average Salary Trends Over Years', showlegend=True)

# Streamlit rendering
st.plotly_chart(fig2)
