import streamlit as st
import pandas as pd
import os
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Superstore' , page_icon=':bar_chart:' , layout = 'wide')
st.title(' :bar_chart: Superstore Data')


st.markdown('<style>div.block-container{padding-top:3rem;}</style>' , unsafe_allow_html=True)
f1 = st.file_uploader(" :file_folder: Upload a file ",type=(['csv' , 'txt' , 'xls' , 'xlsx']))
if f1 is not None:
    filename = f1.name # not understand
    st.write(filename)
    df = pd.read_csv(filename , encoding = 'ISO-8859-1')
else:
    os.chdir(r"D:\Study\Machine Learning Projects\Plotly Dashboard")
    df = pd.read_csv('Sample - Superstore.csv' , encoding = 'ISO-8859-1')

# dealing with datetime

# st.dataframe(df)
col1 , col2 = st.columns(2)
df['Order Date'] = pd.to_datetime(df['Order Date'] , dayfirst=True)

# getting min and max value
startdate = pd.to_datetime(df['Order Date']).min()
enddate = pd.to_datetime(df['Order Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date" , startdate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date" , enddate))

df = df[(df['Order Date'] >= startdate) & (df['Order Date'] <= enddate)].copy()

#filters
st.sidebar.header("Choose your filter : ")

# Create for Region
region = st.sidebar.multiselect("Pick your region" , df['Region'].unique())

if not region:
    df2 = df.copy()

else:
    df2 = df[df['Region'].isin(region)].copy()

# Create for State
state = st.sidebar.multiselect("Pick the state" , df2['State'].unique())

if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)].copy()

# Create for city

city = st.sidebar.multiselect("Pick the city",df3['City'].unique())


# filter data based on region , city and state
# not understand
if not region and not state and not city :
    filtered_df = df
    
elif not region and not city:
    filtered_df = df[df['State'].isin(state)] 

elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]

elif state and city:
    filtered_df = df3[df['State'].isin(state) & df3['City'].isin(city)]

elif region and city:
    filtered_df = df3[df['Region'].isin(region) & df3['City'].isin(city)]

elif region and state:
    filtered_df = df3[df['Region'].isin(region) & df3['State'].isin(state)]

elif city:
    filtered_df = df3[df['City'].isin(city)]

else:
    filtered_df = df3[df3['Region'].isin(region) & df3['City'].isin(city) & df3['State'].isin(state)]

category_df = filtered_df.groupby('Category' , as_index=False)['Sales'].sum()
st.dataframe(category_df)

with col1:
    st.subheader('Category wise sales')
    fig = px.bar(category_df , x = 'Category' , y = 'Sales' , text = ['${:,.2f}'.format(x) for x in category_df['Sales']] )
    st.plotly_chart(fig , width = 'stretch') # plotly_chat() => inbuilt function of streamlit to display plotly charts

with col2:
    st.subheader("Region wise sales")
    fig = px.pie(filtered_df , values='Sales' , names = 'Region' , hole = 0.5)
    fig.update_traces(text = filtered_df['Region'] , textposition = 'outside')
    st.plotly_chart(fig,width = 'stretch')

# downloading and view button
cl1 , cl2 = st.columns(2)
with cl1:
    with st.expander("Category Wise Data"):
        st.write(category_df.style.background_gradient(cmap='Blues'))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download data" , data = csv , file_name='Categorty wise Data.csv' , mime='text/csv' , help='Click here to download the category wise data')

with cl2:
    with st.expander("region Wise Data"):
        region = filtered_df.groupby('Region' , as_index=False )['Sales'].sum()
        st.write(region.style.background_gradient(cmap='Oranges'))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download data" , data = csv , file_name='Region wise Data.csv' , mime='text/csv' , help='Click here to download the regio wise data')

# monthly analysis

filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
st.subheader('Time Series Analysis')

linechart = (filtered_df.groupby(filtered_df['month_year'].dt.strftime("%Y : %b"))['Sales'].sum()).reset_index()
fig2 = px.line(linechart , x = 'month_year' , y = 'Sales' , labels={'Sales' : 'Amount' , 'month_year' : 'Month-Year'} , height=500 , width = 1000 , template='gridon')
st.plotly_chart(fig2 , width = 'stretch')

with st.expander("View Data of Time series:"):
    st.write(linechart.T.style.background_gradient(cmap='magma'))
    csv = linechart.to_csv(index=False).encode('utf-8')
    st.download_button("Download data" , data = csv , file_name='Time Series Data.csv' , mime='text/csv' , help='Click here to download the Time series data')


#  create a treemap
st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(filtered_df , path = ['Region' , 'Category' , 'Sub-Category'] , values='Sales' , hover_data=['Sales'] , color='Sub-Category')
fig3.update_layout(width = 800 , height = 700)
st.plotly_chart(fig3 , width='stretch')

# charts
chart1 , chart2 = st.columns(2)

with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df , values = 'Sales' , names = 'Segment' , template='plotly_dark')
    fig.update_traces(text = filtered_df['Segment']  , textposition = 'inside')
    st.plotly_chart(fig , width = 'stretch')


with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtered_df , values = 'Sales' , names = 'Category' , template='plotly_dark')
    fig.update_traces(text = filtered_df['Category']  , textposition = 'inside')
    st.plotly_chart(fig , width = 'stretch')

# other stuff
import plotly.figure_factory as ff

st.subheader(':point_right: Month-wise sub category sales summary')
with st.expander('Summary Table'):
    df_sample = df.sample(10)[['Region' , 'State' , 'City' , 'Category' , 'Sales' , 'Profit' ,'Quantity']]
    fig = ff.create_table(df_sample , colorscale='viridis')
    st.plotly_chart(fig , width='stretch')

    with st.expander('Month wise sub-category Table'):
        filtered_df['month'] = filtered_df['Order Date'].dt.month_name()
        sub_category_year = pd.pivot_table(data = filtered_df , values='Sales' , index = ['Sub-Category'] ,columns='month' )
        csv = sub_category_year.to_csv().encode('utf-8')
        st.write(sub_category_year.style.background_gradient(cmap='Blues'))
        st.download_button("Download data" , data = csv , file_name='Month wise sub-category Data.csv' , mime='text/csv' , help='Click here to download the Month wise sub-category data')


# scatter plot
st.subheader('Relationship between sales and profit using scatter plot')
data1 = px.scatter(filtered_df , x = 'Sales' , y = "Profit" , size = 'Quantity')
st.plotly_chart(data1 , width = 'stretch')

# download specific part of data
with st.expander('View Data'):
    st.write(filtered_df.sample(500).style.background_gradient(cmap='Greens'))

# dwonload original data
data = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Entire data' , data = data , file_name='Entire Data.csv' , mime = 'text/csv' , help='Download original dataset')