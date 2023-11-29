import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 0. Config the page
st.set_page_config(page_title='Data Science App', page_icon='🧊', layout='wide',)

# 1. Load the data
@st.cache_data()
def load_data():
    url='data/Top_rated_movies1.csv'
    df = pd.read_csv(url, parse_dates=['release_date'])
    return df

# 2. build the UI
st.title("Data Science App")
with st.spinner("Loading data..."):
    df = load_data()

st.header("IMDB 8000 Movies Dataset")
st.info("Raw data in dataframe")
st.dataframe(df, use_container_width=True)

st.success("Column information of the dataset")
cols = df.columns.tolist()
st.subheader(f'Total columns {len(cols)} ➡️ {", ".join(cols)}')

# 3. add some graph and widgets
st.header("Basic Data Visualization")

# graph options
gop = ['bar', 'line', 'area']
# sel_op = st.selectbox('Select the type of plot', gop)

c1, c2 = st.columns(2)            # means set c1 the half of the screen

# column - 1
sel_op = c1.radio('Select the type of plot for popularity', gop, horizontal=True)
subset = df.sort_values(by='popularity')[:50]
if sel_op == gop[0]:
    fig = px.bar(subset, x='title', y='popularity', log_y=True)
elif sel_op == gop[1]:
    fig = px.line(subset, x='title', y='popularity')
elif sel_op == gop[2]:
    fig = px.area(subset, x='title', y='popularity')
c1.plotly_chart(fig, use_container_width=True)

# column - 2
sel_op2 = c2.selectbox('Select the type of plot for vote count', gop)
subset2 = df.sort_values(by='vote_count')[:50]
if sel_op2 == gop[0]:
    fig = px.bar(subset2, x='title', y='vote_count', log_y=True)
elif sel_op2 == gop[1]:
    fig = px.line(subset2, x='title', y='vote_count')
elif sel_op2 == gop[2]:
    fig = px.area(subset2, x='title', y='vote_count')
c2.plotly_chart(fig, use_container_width=True)

# 4. adjust layout

# to include tabs
t1, t2, t3 = st.tabs(['Bivariate', 'Trivariate', 'About'])
num_cols = df.select_dtypes(include=np.number).columns.tolist()

with t1:
    c1, c2 = st.columns(2)
    col1 = st.radio("Select the first column for scatter plot", num_cols)
    col2 = st.radio("Select the second column for scatter plot", num_cols)
    fig = px.scatter(df, x=col1, y=col2, title=f'{col1} vs {col2}')
    st.plotly_chart(fig, use_container_width=True)

with t2:
    c1, c2, cs = st.columns(3)
    col1 = st.selectbox("Select the first column for scatter plot for 3rd plot", num_cols)
    col2 = st.selectbox("Select the second column for scatter plot for 3rd plot", num_cols)
    col3 = st.selectbox("Select the third column for scatter plot for 3rd plot", num_cols)
    fig = px.scatter_3d(df, x=col1, y=col2,z=col3, title=f'{col1} vs {col2} vs {col3}', height=700)
    st.plotly_chart(fig, use_container_width=True)
    
# open terminal and run :
# streamlit run main.py