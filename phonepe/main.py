import streamlit as st
from streamlit_option_menu import option_menu
# Multi page initialization
import home,state_data,transaction_data,user_data,visual_data

st.set_page_config(page_title='Phonepe pulse Data Visualization')
# Initialize a class
class Multiapp:
    def __init__(self):
        self.apps = []
    def add_app(self,title,function):
        self.apps.append({
            "title":title,
            "function":function
        })

    def run():
# Inputs for Side bar option 
        with st.sidebar:
            app = option_menu(
            menu_title='Visualization',
            options=["Home","Transaction","User","State wise Growth","Data Visualization"],
            menu_icon='cast',
            icons=['house','credit-card','person','bar-chart','bar-chart'],
            default_index=1
    )
            
# Function call for use other pages
        if app=='Home':
            home.app()
        elif app=='Transaction':
            transaction_data.app()
        elif app=='User':
            user_data.app()
        elif app=='State wise Growth':
            state_data.app()
        elif app=='Data Visualization':
            visual_data.app()

    run()