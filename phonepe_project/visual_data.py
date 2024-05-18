import streamlit as st
import pandas as pd
import plotly.express as px
import json
import mysql.connector
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Database Connection
mydb = mysql.connector.connect(host="localhost",user="root",password="")
print(mydb)
mycursor = mydb.cursor(buffered=True)

def app():
    st.title(":red[Data Visualization]")
    st.write(":green[Insights]")

    # Query from various insights which get from data

    query_select = st.selectbox(":violet[Select Your Query]",("Select the Query","Top 10 States with Highest Total count 2023",
                                "Top 10 States with Lowest Total count 2023","Top 10 Register users In 2023","State wise Transaction Amount",
                                "State wise Transaction count distribution",
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
        st.write("Insights:")
        st.write("- The top state with the highest total count in 2023 is:", states[0])
        st.write("- :orange[Urbanization and Tech Hubs:] Karnataka is home to major tech cities like Bangalore (Bengaluru), which is of ten referred to as the Silicon Valley of India. These urban centers have a higher concentration of tech-savvy individuals who are more likely to adopt digital payment platforms like PhonePe.")
        st.write("- :orenge[Youth Population:] Karnataka has a relatively young population, with a significant proportion of its residents being young professionals and students. Younger demographics are generally more open to adopting new technologies, including digital payment solutions.")
        st.write("- The difference in total counts between the top state and the 10th state is:", total_counts[0] - total_counts[9])
        st.write("- This visualization helps identify the distribution of transactions across states.")

    elif query_select=="Top 10 States with Lowest Total count 2023":
        st.write(":orange[Top 10 States with Lowest Total count 2023]")
        # Execute the SQL query
        mycursor.execute("SELECT State,Pincode,SUM(Total_count) AS Total_Count FROM phonepe_data.top_trans \
                        Where Year=2023\
                        GROUP BY State \
                        ORDER BY Total_Count ASC LIMIT 10")

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
        ax.set_title('Top 10 States with LOWEST Total Count 2023')

        # Display the chart in Streamlit
        st.pyplot(fig)
        st.write("Insights:")
        st.write("- The state with the lowest total count in 2023 is:", states[0])
        st.write("-  :orange[Geographical Constraints:] Lakshadweep is a group of islands with a small land area and population. The limited physical infrastructure and remoteness of the islands may restrict economic activities and, consequently, digital transactions.")
        st.write("-  :orange[Population Size:] Lakshadweep has one of the smallest populations among Indian territories. With fewer residents, there may be fewer transactions overall, both in terms of the number of users and the volume of transactions.")
        st.write("- The difference in total counts between the lowest state and the 10th lowest state is:", total_counts[9] - total_counts[0])
        st.write("- Potential reasons for lower transaction counts could include lower population density, lesser economic activity, or slower adoption of digital payment platforms in these states.")
        


 



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
        st.write("Insights:")
        st.write("- The top state with the highest number of registered users in 2023 is:", states[0])
        st.write("- The difference in registered users between the top state and the 10th state is:", register_users[0] - register_users[9])
        st.write("- This visualization provides an overview of user adoption across different states.")
       

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
        st.write("Insights:")
        st.write("- The visualization shows the total transaction amounts across different states from 2018 to 2023.")
        st.write("- States with higher transaction amounts may indicate greater economic activity or higher adoption of digital payment platforms.")
        st.write("- Analyzing trends over time can help identify states that are experiencing significant growth in transaction amounts.")


    elif query_select== "State wise Transaction count distribution":
        st.write(":orange[State wise Transaction count distribution]")
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
        st.write("Insights:")
        st.write("- The visualization illustrates the distribution of transaction counts across different states and transaction types.")
        st.write("- Examining transaction counts by type can reveal insights into consumer behavior, such as preferences for payment methods or transaction categories.")
        st.write("- Analyzing transaction count distribution can also help identify states with diverse transaction patterns or potential areas for targeted interventions.")


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
        st.write("Insights:")
        st.write("- The visualization displays the trends in transaction types over the years.")
        st.write("- Analyzing transaction type counts over time can reveal shifts in consumer behavior or changes in the usage of different payment methods.")
        st.write("- Trends such as increasing or decreasing transaction counts for specific types can indicate evolving preferences or market dynamics.")


    elif query_select=="State wise Transaction count over Years":
        mycursor.execute("SELECT State, Year, SUM(Transaction_count) AS Transaction_count FROM phonepe_data.aggregate_trans \
                 GROUP BY State, Year")
        out = mycursor.fetchall()

        # Close the database connection
        mydb.commit()

        # Convert fetched data to DataFrame
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        # Visualize the data using Plotly
        fig = go.Figure()

        fig = px.bar(df, x=df.State, y=df.Transaction_count, color=df.Year,title='State wise transaction count over Years',height=750)
        st.plotly_chart(fig)
        st.write("Insights:")
        st.write("- The visualization illustrates how transaction counts have varied across different states over the years.")
        st.write("- Examining transaction counts by state and year can reveal insights into regional trends and the growth of digital transactions.")
        st.write("- States with significant increases in transaction counts may indicate strong adoption of digital payment platforms or increasing economic activity.")

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
        st.write("Insights:")
        st.write("- The visualization represents the distribution of users among different brands.")
        st.write("- Examining the percentage of users by brand can provide insights into brand loyalty or market share.")
        st.write("- Brands with higher percentages may have a larger user base or stronger adoption rates.")


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
        st.write("Insights:")
        st.write("- The visualization represents the distribution of registered users among different states.")
        st.write("- Examining the percentage of register users by state can provide insights into regional adoption rates or user engagement.")
        st.write("- States with higher percentages may have a larger user base or stronger adoption of the platform.")


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
        st.write("Insights:")
        st.write("- The visualization represents the distribution of app openings among different states in 2023.")
        st.write("- Examining app openings by state can provide insights into regional engagement levels or user activity.")
        st.write("- States with higher percentages may have a larger user base or stronger user engagement with the app.")