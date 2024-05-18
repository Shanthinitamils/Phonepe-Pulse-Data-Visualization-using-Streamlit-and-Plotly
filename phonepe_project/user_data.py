import streamlit as st
import pandas as pd
import plotly.express as px
import json
import mysql.connector

# Database Connection

mydb = mysql.connector.connect(host="localhost",user="root",password="")
print(mydb)
mycursor = mydb.cursor(buffered=True)

def app():
    
    # Create a function to load the data

    def load_data(year, quarter):
        query = "SELECT State, SUM(Total_count) AS total_count FROM phonepe_data.aggregate_user \
                WHERE Year = %s \
                GROUP BY State"
        mycursor.execute(query, (year,))
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
                                color='total_count', 
                                color_continuous_scale='Viridis', 
                                range_color=(df1['total_count'].min(), df1['total_count'].max()),
                                mapbox_style='carto-positron', 
                                zoom=4, center={'lat': 22, 'lon': 82})
        fig.update_layout(title=f'Total Transaction User Count by State Year-{year}/Q{quarter}', 
                        title_x=0.5, 
                        margin={'r': 20, 't': 30, 'l': 20, 'b': 20})
        return fig

    # Load the geojson data
    with open(r'C:\Users\HP\Desktop\New folder\Indian_state.json') as f:
        india_states_geojson = json.load(f)

    # Create a Streamlit app
    st.title(":red[Choropleth Map of Total Transaction User Count by State]")
    st.write(":green[Select the year and quarter to display the choropleth map:]")

    years = ["Select the Year",2018, 2019, 2020, 2021, 2022]
    quarters = ["Select the Quater",1, 2, 3, 4]

    year_selected = st.selectbox(":blue[Select the year:]", years)
    quarter_selected = st.selectbox(":blue[Select the quarter:]", quarters)

    df = load_data(year_selected, quarter_selected)
    fig = create_choropleth_map(df, year_selected, quarter_selected)
    on=st.toggle('switch to view')

    if on:
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)
    
   