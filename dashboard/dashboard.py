import streamlit as st 
import pandas as pd
import folium
import os
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from folium.plugins import FastMarkerCluster



st.set_page_config(page_title="E-comerce data analysis", page_icon=":bar_chart:", layout="wide")

# title 
st.title(":bar_chart: E-comerce data analysis")
st.markdown('<style>div.block-conutainer{padding-top:lrem;</style>',unsafe_allow_html=True)

# import file
df = pd.read_csv("RfM_data.csv", encoding="utf-8-bom")  # Example for UTF-8 with BOM



# Set up sidebar
st.sidebar.header("Choose filter: ")

# Create RFM parameter
Rfm = st.sidebar.selectbox(label="Choose RFM Parameter", options=('Recency', 'Frequency', 'Monetary'))
df2 = df.sort_values(by=['rfm_total'], ascending=False)

# Display table
st.subheader('High/Low value customer')
options = st.selectbox(
    label="Order by",
    options=('Highest', 'Lowest')
)
# Choose order by highest/lowest
if options == 'Highest':
    Type1 = df.sort_values(by=['rfm_total'], ascending=False)
    st.write(Type1)
else:
    Type2 = df.sort_values(by=['rfm_total'], ascending=True)
    st.write(Type2)

# Set up columns
col1, col2 = st.columns((2)) 

#Column 1 Top customer with total rfm = 9
with col1:
    st.subheader(':trophy: Top customer')

# Create visualiztaion base on RFM parameter
    sorted_df = df.sort_values(by=['rfm_total'], ascending=False)

    # Select the top 5 customers
    top_customers = sorted_df.head()

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.barplot(x=top_customers['customer_random_name'], y=top_customers[Rfm], ax=ax)
    plt.xlabel('Customer_random_name')
    plt.ylabel(Rfm)
    plt.title(f'Top 5 Customers by {Rfm}')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # create annotation in bar 
    for p in ax.patches:
        plt.gca().annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='center', xytext=(0, 10), textcoords='offset points') 

    st.pyplot(fig)

# Column 2 customer type distribution
with col2:
    st.subheader('Customer Type Distribution')

    # Create countplot   
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.countplot(x='customer_type', data=df, order=df['customer_type'].value_counts().index)
    plt.title('Distribution by Customer Type')
    plt.xlabel('Customer Type')
    plt.ylabel('Number of Customers')

    # Annotate bar heights
    for p in ax.patches:
        plt.gca().annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='center', xytext=(0, 10), textcoords='offset points') 

    st.pyplot(fig)


# Creating map to visualize each customer location 
st.subheader(":earth_americas: Customer distribution by region")

map = folium.Map(location=[-8.783195, -55.491478], zoom_start=2)

FastMarkerCluster(data=list(zip(df['geolocation_lat'], df['geolocation_lng']))).add_to(map)

st_folium(map, width= 1000, height=500)
