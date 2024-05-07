import streamlit as st
import numpy as np
# Introduction about PHonepe
def app():
    st.title(":blue[Phonepe Pulse Data Visualization]")
    st.subheader(":orange[PhonePe: A Leading Digital Wallet in India]")
    st.write("Introducing PhonePe, a safe and user-friendly digital wallet that allows quick money transfers in multiple languages.")

    st.write(":orange[Key Benefits of PhonePe]")
    st.write("1. **Safe and Secure:** PhonePe follows industry-standard security measures to protect your transactions.")
    st.write("2. **Easy to Use:** The app is designed to be user-friendly and requires minimal time to get accustomed to.")
    st.write("3. **Multi-language Support:** PhonePe is available in multiple local Indian languages for a more personalized experience.")
    st.write("4. **24/7 Availability:** Transfer money anytime, anywhere, without any hassle.")

    st.write(":orange[Active Users Over Time]")
    users_over_time = [1000, 2500, 5000, 10000, 20000, 35000, 50000]  # Replace this with actual data
    st.bar_chart(users_over_time)

    

    st.write(":orange[Most Popular Languages]")
    popular_languages = ['Hindi', 'English', 'Tamil', 'Telugu', 'Marathi']  # Replace this with actual data
    st.bar_chart(popular_languages)
  