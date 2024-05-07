import streamlit as st
import pandas as pd
import plotly.express as px
import json
import mysql.connector
import matplotlib.pyplot as plt

# Database Connection
mydb = mysql.connector.connect(host="localhost",user="root",password="")
print(mydb)
mycursor = mydb.cursor(buffered=True)

def app():
    st.title(":blue[Data Visualization]")
    st.write(":green[Insights]")

    # Query from various insights which get from data

    query_select = st.selectbox(":violet[Select Your Query]",("Select the Query","Top 10 States with Highest Total count 2023",
                                "Top 10 Register users In 2023","State wise Transaction Amount",
                                "Satae wise Transaction count distribution",
                                "Transaction type count over the Years",
                                "State wise Transaction count over Years",
                                "Percentage of Users Brand wise",
                                "State wise Register User",
                                "State wise App opened Data"))
    
    if query_select=="Select the Query:":
        st.write("  ")

    elif query_select=="Top 10 States with Highest Total count 2023":
        st.write(":orange[Top 10 States with Highest Total count 2023]")
        # Execute the SQL query
        mycursor.execute("SELECT State,Pincode,SUM(Total_count) AS Total_Count FROM phonepe_data.top_trans \
                        Where Year=2023\
                        GROUP BY State \
                        ORDER BY Total_Count DESC LIMIT 10")

        # Fetch the results
        states = []
        total_counts = []
        for row in mycursor.fetchall():
            states.append(row[0])
            total_counts.append(row[2])

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(15,6))
        ax.bar(states, total_counts)
        ax.set_xlabel('State')
        ax.set_ylabel('Total Count')
        ax.set_title('Top 10 States with Highest Total Count 2023')

        # Display the chart in Streamlit
        st.pyplot(fig)



    elif query_select=="Top 10 Register users In 2023":
        st.write(":orange[Top 10 Register users In 2023]")
        # Execute the SQL query
        mycursor.execute("SELECT State,Pincode,SUM(Register_user) AS Register_User FROM phonepe_data.top_user \
                        Where Year=2023\
                        GROUP BY State \
                        ORDER BY Register_User DESC LIMIT 10")

        # Fetch the results
        states = []
        register_users = []
        for row in mycursor.fetchall():
            states.append(row[0])
            register_users.append(row[2])

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(15,6))
        ax.bar(states, register_users)
        ax.set_xlabel('State')
        ax.set_ylabel('Register Users')
        ax.set_title('Top 10 States with Highest Register Users 2023')

        # Display the chart in Streamlit
        st.pyplot(fig)


    elif query_select=="State wise Transaction Amount":
        st.write(":orange[State wise Transaction Amount]")
        # Execute the SQL query
        mycursor.execute("SELECT State,Year,Transaction_amount FROM phonepe_data.aggregate_trans\
                        where year between 2018 and 2023\
                        Group by State")

        # Fetch the results
        out = mycursor.fetchall()

        # Close the database connection
        mydb.commit()

        # Convert fetched data to DataFrame
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        # Create a bar chart using Plotly
        fig = px.bar(df, x=df.State, y=df.Transaction_amount, color=df.State,title='State wise transaction amount in Billions for year 2018',height=750)

        # Display the chart in Streamlit
        st.plotly_chart(fig)


    elif query_select== "Satae wise Transaction count distribution":
        st.write(":orange[Satae wise Transaction count distribution]")
        # Execute the SQL query
        mycursor.execute("SELECT State,Year,Transaction_type,SUM(Transaction_count) Transaction_count FROM phonepe_data.aggregate_trans \
                        Group by State,Transaction_type")

        # Fetch the results
        out = mycursor.fetchall()

        # Close the database connection
        mydb.commit()

        # Convert fetched data to DataFrame
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        # Create a bar chart using Plotly
        fig = px.bar(df, x=df.State, y=df.Transaction_count, color=df.Transaction_type,title='State wise transaction count distribution',height=750)

        # Display the chart in Streamlit
        st.plotly_chart(fig)


    elif query_select== "Transaction type count over the Years":
        st.write(":orange[Transaction type count over the Years]")
        # Execute the SQL query
        mycursor.execute("SELECT Year,Transaction_type,SUM(Transaction_count) Transaction_count FROM phonepe_data.aggregate_trans \
                        Group by Year,Transaction_type")

        # Fetch the results
        out = mycursor.fetchall()

        # Close the database connection
        mydb.commit()

        # Convert fetched data to DataFrame
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        # Create a bar chart using Plotly
        fig = px.bar(df, x=df.Transaction_type, y=df.Transaction_count, color=df.Year,title='Transaction type count over the years',height=750)

        # Display the chart in Streamlit
        st.plotly_chart(fig)


    elif query_select=="Percentage of Users Brand wise":
        st.write(":orange[Percentage of Users Brand wise]")
        # Execute the SQL query
        mycursor.execute("SELECT State,Year,sum(Percentage) as Percentage,Brand FROM phonepe_data.aggregate_user\
                        GROUP BY State,Brand")

        # Fetch the results
        out = mycursor.fetchall()

        # Close the database connection
        mydb.commit()

        # Convert fetched data to DataFrame
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        # Create a pie chart using Plotly
        fig = px.pie(df, values='Percentage', names='Brand',color_discrete_sequence=px.colors.sequential.RdBu,title='Percentage of User Brand wise')
        fig.update_traces(textposition='inside', textinfo='percent+label')

        # Display the chart in Streamlit
        st.plotly_chart(fig)


    elif query_select=="State wise Register User":
        st.write(":orange[State wise Register User]")
        # Execute the SQL query
        mycursor.execute("SELECT State,SUM(Register_user) as Registeruser FROM phonepe_data.map_user \
                        Group BY State ")

        # Fetch the results
        out = mycursor.fetchall()

        # Close the database connection
        mydb.commit()

        # Convert fetched data to DataFrame
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        # Create a pie chart using Plotly
        fig = px.pie(df, values='Registeruser', names='State',title='State wise Register User')
        fig.update_traces(textposition='inside', textinfo='percent+label')

        # Display the chart in Streamlit
        st.plotly_chart(fig)


    elif query_select=="State wise App opened Data":
        st.write(":orange[State wise App opened Data]")
        # Execute the SQL query
        mycursor.execute("SELECT State,SUM(Register_user) as Registeruser,SUM(App_opened) as App_open FROM phonepe_data.map_user \
                        where year=2023 \
                        Group BY State")

        # Fetch the results
        out = mycursor.fetchall()

        # Close the database connection
        mydb.commit()

        # Convert fetched data to DataFrame
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        # Create a pie chart using Plotly
        fig = px.pie(df, values='App_open', names='State',title='State wise App opened Data')
        fig.update_traces(textposition='inside', textinfo='percent+label')

        # Display the chart in Streamlit
        st.plotly_chart(fig)