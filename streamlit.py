import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
from utils import add_round, get_handicaps, fill_handicaps, plot_statistics, histplot, pie_chart, dist_plot, rolling_avg, scatter, mean_med_stats, find_round, handicap_differentials, total_profit, explanation_of_plots, agg_features_by_cat, add_border

from dashboard import dashboard

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
    add_border()

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

    column_order = ["name", "date", "golf_course", "match_format", "opponent/s", "profit/loss", "course_rating", "slope_rating",
                    "adj_gross_score", "handicap_diff", "putts", "3_putts", "fairways_hit", "gir", "penalty/ob", "birdies", "trpl_bogeys_plus",
                   "handicap", "notes", "jittered_col"]
# -------------------------------------------------------------- Fake Data ------------------------------------------------------------
    
    # Change data source depending on tab selection
    if selected == "Fake Data":
        # Data load
        if "df" not in st.session_state:
            st.session_state.df = pd.read_csv("synthetic_data.csv", parse_dates=["date"])
            st.session_state.df = st.session_state.df.reindex(columns=column_order)
    
        st.subheader(":blue[While my friends and I collect some data...]")
        st.markdown("""I have generated some synthetic data to demonstrate the visualizations we will use to track and analyze our scores. This data is purely for purposes of demonstration, and some of the statistics and relationships shown will likely not reflect reality for most golfers. """)
        explanation_of_plots()

        
        add_border()        
        # Give the option to add data
        st.subheader(":blue[Add your own data?:]")

        
        col1, col2 = st.columns([1,1])
        with col1:
            rd_name = st.text_input("Name:", value="[name]")
            rd_date = st.date_input("Date Played:", min_value = pd.to_datetime("2024-04-13"))
            rd_adj_score = st.number_input("Adjusted Gross Score (Must know single hole limits)", min_value=60, value=72, step=1)
            rd_cr_rating = st.number_input("Course Rating:", min_value=60.0, max_value=90.0, value=72.0)
            rd_slope_rating = st.number_input("Slope Rating:", min_value=55.0, max_value=155.0, value=113.0)
            rd_putts = st.number_input("Number of Putts:", step=1, value=36)
            rd_three_putts = st.number_input("Number of 3-Putts:", step=1)
            rd_opponent = st.text_input("Opponent/s:", value="[opponent name]")
            rd_notes = st.text_input("Notes about the round:", value="[notes]", max_chars= 200)
        with col2:
            rd_fairways = st.number_input("Number of Fairways Hit:", step=1)
            rd_gir = st.number_input("Number of Greens in Regulation:", step=1)
            rd_penalty = st.number_input("Number of Penalty Shots:", step=1)
            rd_birdies = st.number_input("Number of Birdies:", step=1)
            rd_db_bogeys_plus = st.number_input("Number of Triple-Bogeys or Worse:", step=1)
            profit_loss = st.number_input("Profit/Loss (in betting units)")
            match_format = st.selectbox("Match Format:", [None, "Match Play", "Skins", "Stroke Play", "Dots", "Nassau"])
            rd_golf_course = st.selectbox("Golf Course:", ["Augusta National", "Pebble Beach", "Bethpage Black", "Kiawah Island", 
                                                            "Whistling Straits", "Pinehurst", "Hollybrook", "Harbortown"])
    
        # Button click logic
        if "button_clicked" not in st.session_state:
            st.session_state.button_clicked = False
        
        def button_click():
            st.session_state.button_clicked = True
    
        if st.button("Add Round?"):
            
            # Add the round to the df
            new_row = add_round(name=rd_name, date=str(rd_date), adj_gross_score=rd_adj_score, course_rating=rd_cr_rating,
                                slope_rating=rd_slope_rating, putts=rd_putts, three_putts=rd_three_putts, fairways=rd_fairways, gir=rd_gir,
                                penalties=rd_penalty, birdies=rd_birdies, trpl_bogeys_plus=rd_db_bogeys_plus, profit_loss=profit_loss, 
                                match_format=match_format, golf_course=rd_golf_course, calc_diff=True)


            new_row_df = pd.DataFrame([new_row])
    
            # Add row to the df
            st.session_state.df = pd.concat([st.session_state.df, new_row_df], ignore_index=True)
            
            # Update handicaps where applicable
            st.session_state.df = get_handicaps(st.session_state.df)
    
            
            st.write("Check out your new entry at the bottom of the dataframe")
    
            # Change the boolean status to display a df
            button_click()

            if st.session_state.button_clicked:
                st.dataframe(st.session_state.df.loc[st.session_state.df["name"] == rd_name].drop(columns="jittered_col"), hide_index=True,
                             use_container_width=True)
    
        
        # Run the rest of the dashboard
        dashboard(st.session_state.df)
    


# -------------------------------------------------------------- Real Data ------------------------------------------------------------    
    elif selected == "Real Data":
        df = pd.read_csv("real_data.csv", parse_dates=["date"])

        df = df.reindex(columns=column_order)
        
        # Temporarily stopping until sufficient data has been collected
        # st.stop()  
        
        explanation_of_plots()

        st.subheader(":red[We are still collecting data currently, please bear with us.]")
        st.write('Switch back to the "Fake Data" tab to see all of the available visualizations with a larger (synthetic) dataset.')

        st.markdown("""<hr style="border: 2px solid #40a3ff">""", unsafe_allow_html=True)
        st.subheader(":red[Handicaps are still pending until a sufficient number of rounds have been played...]")
        dashboard(df)

    
    
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