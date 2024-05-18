import streamlit as st
import pandas as pd
import plotly.express as px
import json
import mysql.connector
import plotly.io as pio
import plotly.graph_objects as go

# Databse Connection
mydb = mysql.connector.connect(host="localhost",user="root",password="")

print(mydb)
mycursor = mydb.cursor(buffered=True)

def app():


    # Create a function to create the line plot
    def load_data(state):
        query = "SELECT State, Year, SUM(Transaction_count) AS Transaction_Count FROM phonepe_data.aggregate_trans \
                WHERE State=%s \
                GROUP BY Year"
        mycursor.execute(query, (state,))
        out = mycursor.fetchall()
        mydb.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        return df

    # Create a function to create the line plot
    def create_line_plot(df):
        trace = go.Scatter(
            x=df['Year'],
            y=df['Transaction_Count'],
            mode='lines',
            name=df['State'].values[0]
        )

        layout = go.Layout(
            title='Transaction Count by Year for ' + df['State'].values[0],
            xaxis=dict(title='Year'),
            yaxis=dict(title='Transaction Count')
        )

        fig = go.Figure(data=[trace], layout=layout)

        return fig

    # Create a Streamlit app
    st.title(":red[Transaction Count by Year for Each State]")
    st.write(":green[Select the state to display the transaction count by year:]")

    states = ['Andaman & Nicobar','Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Lakshadweep', 'Puducherry']

    state_selected = st.selectbox(":blue[Select the state:]", states)

    df = load_data(state_selected)
    fig = create_line_plot(df)

    on=st.toggle('switch to view')

    if on:
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df)
        st.write("Insights:")
        st.write("- The line plot represents the transaction count by year for the selected state.")
        st.write("- Observing trends over time can reveal patterns such as growth, decline, or stability in transaction counts.")
        st.write("- Significant fluctuations in transaction counts may indicate changes in consumer behavior, economic factors, or platform usage.")