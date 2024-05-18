import streamlit as st
import pandas as pd
import plotly.express as px
import json
import mysql.connector
import time

# Database connection
mydb = mysql.connector.connect(host="localhost",user="root",password="")

print(mydb)
mycursor = mydb.cursor(buffered=True)

def app():

    # Load the geojson data
    with open(r'C:\Users\HP\Desktop\New folder\Indian_state.json') as f:
        india_states_geojson = json.load(f)

    # Create a function to load the data
    def load_data(year, quarter):
        query = "SELECT State, SUM(Transaction_amount) AS transaction_amount FROM phonepe_data.aggregate_trans \
                WHERE Year = %s and Quarter = %s \
                GROUP BY State"
        mycursor.execute(query, (year, quarter))
        out = mycursor.fetchall()
        mydb.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])
        
        return df

    # Create a function to create the choropleth map
    def create_choropleth_map(df, year, quarter):
        df_geo = pd.json_normalize(india_states_geojson['features']).rename(columns={'properties.ST_NM': 'State'})
        df1 = pd.merge(df, df_geo, on='State')
        fig = px.choropleth_mapbox(df1, geojson=india_states_geojson, 
                                locations='State', 
                                featureidkey='properties.ST_NM',
                                color='transaction_amount', 
                                color_continuous_scale='Viridis', 
                                range_color=(df1['transaction_amount'].min(), df1['transaction_amount'].max()),
                                mapbox_style='carto-positron', 
                                zoom=3, center={'lat': 22, 'lon': 82})
        fig.update_layout(title=f'Total Transaction Amount by State Year-{year}/Q{quarter}', 
                        title_x=0.5, 
                        margin={'r': 20, 't': 30, 'l': 20, 'b': 20})
        return fig

    # Create a Streamlit app
    st.title(":red[Choropleth Map of Transaction Amount by State]")
    st.write(":green[Select the year and quarter to display the choropleth map:]")

    years = ["Select the Year",2018, 2019, 2020, 2021, 2022, 2023]
    quarters = ["Select the Quarter",1, 2, 3, 4]
    
    year_selected = st.selectbox(":blue[Select the year:]", years)
    quarter_selected = st.selectbox(":blue[Select the quarter:]", quarters)

    df = load_data(year_selected, quarter_selected)
    fig = create_choropleth_map(df, year_selected, quarter_selected)

    
    on=st.toggle('switch to view')

    if on:
        col1,col2=st.columns([2,1])
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(df)