import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
from utils import add_round, get_handicaps, fill_handicaps, plot_statistics, histplot, pie_chart, dist_plot, rolling_avg, scatter, mean_med_stats, find_round, handicap_differentials, total_profit, explanation_of_plots

from fake_data import fake_data

from real_data import real_data

from background import background_info

from streamlit_option_menu import option_menu

def main():

    # Config page layout
    st.set_page_config(page_title="Golf Group Handicap Tracker",
                   page_icon=':golf:',
                      layout="wide")
    
    # Page Title Text, Subtitle
    st.title(':orange[Golf Group Handicap Tracker]')
    st.subheader(":silver[_Statistics to Inform and Expedite Match Negotiations_]")
    st.markdown("---")

    # Display the body paragraphs from background.py
    background_info()


# -------------------------------------------------------------- Data Selection ------------------------------------------------------------    
    # Tabs for data sources
    selected = option_menu(
        menu_title=None,
        options=['Fake Data', 'Real Data'],
        icons=['bar-chart-fill', 'person-fill'],  # 'bar-chart-fill', 'person-fill'
        orientation='horizontal',
    )


# -------------------------------------------------------------- Fake Data ------------------------------------------------------------
    
    # Change data source depending on tab selection
    if selected == "Fake Data":
        # Data load
        if "df" not in st.session_state:
            st.session_state.df = pd.read_csv("synthetic_data.csv", parse_dates=["date"])        
    
        st.subheader(":blue[While my friends and I collect some data...]")
        st.markdown("""I have generated some synthetic data to demonstrate the visualizations we will use to track and analyze our scores. This data is purely for purposes of demonstration, and some of the statistics and relationships shown will likely not reflect reality for most golfers. """)
        explanation_of_plots()

        fake_data()
    


# -------------------------------------------------------------- Real Data ------------------------------------------------------------    
    elif selected == "Real Data":
        df = pd.read_csv("real_data.csv", parse_dates=["date"])
        
        st.subheader(":red[We are still collecting data currently, please bear with us.]")
        st.write('Switch back to the "Fake Data" tab to see all of the available visualizations')
        
        # Temporarily stopping until sufficient data has been collected
        st.stop()  
        
        explanation_of_plots()
        real_data()

    
    
    # ------------------------------------- Sidebar - Bio info -------------------------------------------------
    st.sidebar.title('About Me:')
    
    # Variables for f-strings
    linkedin_url = "https://www.linkedin.com/in/david-hartsman-data/"
    github_url = "https://github.com/dvdhartsman"
    medium_url = "https://medium.com/@dvdhartsman"
    
    linkedin_markdown = f'[LinkedIn]({linkedin_url})'
    github_markdown = f'[GitHub]({github_url})'
    medium_markdown = f'[Blog]({medium_url})'
    
    # Text display
    st.sidebar.subheader('David Hartsman')
    st.sidebar.markdown(f"{linkedin_markdown} | {github_markdown} | {medium_markdown}", unsafe_allow_html=True)
    st.sidebar.write('dvdhartsman@gmail.com')
    



if __name__ == "__main__":
    main()