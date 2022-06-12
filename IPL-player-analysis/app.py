import streamlit as st
# from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


st.title('IPL Cricket Stats (Player Rankings)')
st.write('---')


# image = Image.open('/Users/aditya/Downloads/streamlit/ipl-cricket-app/images/ipl-logo.jpg')

# st.image(image, width=700)

# st.markdown("""
# This app performs simple webscraping of IPL Cricket player stats data (focussing on player rankings)!
# * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
# * **Data source:** [Cricmetric](http://www.cricmetric.com/ipl/ranks/).
# * For more information about the statistics, refer to the [glossary](http://www.cricmetric.com/blog/glossary/).
# """)

st.header('Display Player Stats of All Teams')

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2008, 2021))))

# Web scraping of IPL player stats
# http://www.cricmetric.com/ipl/ranks/2020


@st.cache
def load_data(year):
    url = "http://www.cricmetric.com/ipl/ranks/" + str(year)
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.fillna('NA')
    playerstats = raw
    return playerstats


playerstats = load_data(selected_year)
playerstats

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Team.unique())
selected_team = st.sidebar.multiselect(
    'Team', sorted_unique_team, sorted_unique_team)

# Filtering data
df_selected_team = playerstats[(playerstats.Team.isin(selected_team))]

st.markdown("""
* **Data source:** [Cricmetric](http://www.cricmetric.com/ipl/ranks/).
* For more information about the statistics, refer to the [glossary](http://www.cricmetric.com/blog/glossary/).
""")

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(
    df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download IPL player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806


def filedownload(df):
    csv = df.to_csv(index=False)
    # strings <-> bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

st.header('**Player Data Analysis**:')


# histogram
if st.button('Histogram Analyses'):
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')
    df['Salary'] = df['Salary'].str.replace(
        ',', '').str.replace('$', '').astype(float)
    df['Value'] = df['Value'].str.replace(
        ',', '').str.replace('$', '').astype(float)
    df = pd.DataFrame(
        df, columns=['RAA', 'Wins', 'EFscore', 'Salary', 'Value'])
    df.hist()
    plt.show()
    st.pyplot()


# Line Chart
if st.button('Comparison between Salary and Value'):
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')
    df['Salary'] = df['Salary'].str.replace(
        ',', '').str.replace('$', '').astype(float)
    df['Value'] = df['Value'].str.replace(
        ',', '').str.replace('$', '').astype(float)
    df = pd.DataFrame(df, columns=['Salary', 'Value'])
    st.line_chart(df)


st.header('**IPL 2022 Qualifier Analysis**:')

if st.button('Comparing Various Models'):
    from PIL import Image
    image = Image.open('models.png')
    st.image(image, caption='Model Fitting', use_column_width=True)

if st.button('Qualifier Results'):
    from PIL import Image
    image = Image.open('result.png')
    st.image(image, caption='Decision tree results', use_column_width=True)

# Bar plot
if st.button('Comparison of teams based on Value of their players'):
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')
    df['Value'] = df['Value'].str.replace(
        ',', '').str.replace('$', '').astype(float)
    fig_dims = (19, 10)
    fig, ax = plt.subplots(figsize=fig_dims)
    sns.barplot(x='Value', y='Team', ax=ax, data=df)
    st.pyplot()


st.write('---')
