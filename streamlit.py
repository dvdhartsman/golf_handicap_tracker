import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
from utils import add_round, get_handicaps, fill_handicaps, plot_statistics, histplot, pie_chart, dist_plot, rolling_avg, scatter, mean_med_stats, find_round, handicap_differentials

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
    
# --------------------------------------------------------------Visualizations------------------------------------------------------------
    
    # Tabs for data sources
    selected = option_menu(
        menu_title=None,
        options=['Fake Data', 'Real Data'],
        icons=['bar-chart-fill', 'person-fill'],  # 'bar-chart-fill', 'person-fill'
        orientation='horizontal',
    )

    # Change data source depending on tab selection
    if selected == "Fake Data":
        # Data load
        if "df" not in st.session_state:
            st.session_state.df = pd.read_csv("synthetic_data.csv", parse_dates=["date"])
        
    
        st.subheader(":blue[While my friends and I collect some data...]")
        st.markdown("""I have generated some synthetic data to demonstrate the visualizations we will use to track and analyze our scores. This data is purely for purposes of demonstration, and some of the statistics and relationships shown will likely not reflect reality for most golfers. \n \nThat being said, I am still the best golfer based on synthetic data......""")
    
    
    elif selected == "Real Data":
        st.subheader(":red[We are still collecting data currently, please bear with us.]")
        st.write('Switch back to the "Fake Data" tab to see all of the available visualizations')
        st.stop()


    st.markdown(":blue[_A brief note about the plots:_]")
    st.markdown("You can isolate a plot component by double-clicking on it in the legend, or you can toggle on/off individual plot items by clicking on the desired item in the legend. You can also click and drag over quadrants of graphs to zoom in on areas of interest. Click the home icon in the upper-right corner or double-click on the plot to zoom back out to the original scope. Finally, as you move your mouse cursor over the plots, you will notice hover-values that display additional information. Thank you and enjoy the dashboard")
        
    st.markdown("---")
        
    # Give the option to add data
    st.subheader(":violet[Add your own data?:]")
    col1, col2 = st.columns([1,1])
    with col1:
        rd_name = st.text_input("Name:", value="[name]")
        rd_date = st.date_input("Date Played:", min_value = pd.to_datetime("2024-04-13"))
        rd_adj_score = st.number_input("Adjusted Gross Score (Must know single hole limits)", min_value=60, value=72, step=1)
        rd_cr_rating = st.number_input("Course Rating:", min_value=60.0, max_value=90.0, value=72.0)
        rd_slope_rating = st.number_input("Slope Rating:", min_value=55.0, max_value=155.0, value=113.0)
        rd_putts = st.number_input("Number of Putts:", step=1)
        rd_three_putts = st.number_input("Number of 3-Putts:", step=1)
    with col2:
        rd_fairways = st.number_input("Number of Fairways Hit:", step=1)
        rd_gir = st.number_input("Number of Greens in Regulation:", step=1)
        rd_penalty = st.number_input("Number of Penalty Shots:", step=1)
        rd_birdies = st.number_input("Number of Birdies:", step=1)
        rd_db_bogeys_plus = st.number_input("Number of Double-Bogeys or Worse:", step=1)
        profit_loss = st.number_input("Profit/Loss (in betting units)")

    # Button click logic
    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False
    
    def button_click():
        st.session_state.button_clicked = True

    if st.button("Add Round?"):
        
        # Add the round to the df
        new_row = add_round(name=rd_name, date=str(rd_date), adj_gross_score=rd_adj_score,
                                                                      course_rating=rd_cr_rating, slope_rating=rd_slope_rating, putts=rd_putts,
                                                                      three_putts=rd_three_putts, fairways=rd_fairways, gir=rd_gir,
                                                                      penalties=rd_penalty, birdies=rd_birdies, 
                                                                      dbl_bogeys_plus=rd_db_bogeys_plus, profit_loss=profit_loss, calc_diff=True)

        new_row_df = pd.DataFrame([new_row])

        # Add row to the df
        st.session_state.df = pd.concat([st.session_state.df, new_row_df], ignore_index=True)
        
        # Update handicaps where applicable
        st.session_state.df = get_handicaps(st.session_state.df)

        
        st.write("Check out your new entry at the bottom of the dataframe")

        # Change the boolean status to display a df
        button_click()

    if st.session_state.button_clicked:
        st.dataframe(st.session_state.df.loc[st.session_state.df["name"] == rd_name].drop(columns="jittered_col"), hide_index=False,
                     use_container_width=True)


    # ------------------- Beginning of Plot Section ------------------------------
    
    # Colors for plots to avoid repeating colors
    color_map = dict(zip([name for name in st.session_state.df["name"].unique()], px.colors.qualitative.Vivid))

    st.dataframe(st.session_state.df)

    # Useful for labels, titles of plots
    label_dict = {
        "adj_gross_score":"Adjusted Gross Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts per Round",
        "3_putts": "3-Putts per Round",
        "fairways_hit": "Fairways Hit per Round",
        "gir": "Greens in Regulation",
        "penalty/ob": "Penalties / OB per Round",
        "handicap":"Handicap Index",
        "birdies":"Birdies",
        "dbl_bogeys_plus":"Double Bogey or Worse",
        "profit/loss":"Profit/Loss"
    }

    # Also useful for labeling, titling, etc.
    reverse_labels = {val:key for key, val in label_dict.items()}


 # -------------------- # Synthetic Data Display ----------------------   
    
    # Numerical handicap displays for each player
    st.markdown("""<div style="text-align: center; font-size:40px; color:gold">
            <b><u><i>Current Player Handicaps:</i></u></b>
            </div>""", unsafe_allow_html=True)
    
    # finding unique players with valid handicaps
    names = st.session_state.df.dropna(subset="handicap")["name"].unique()
    col1, col2, col3 = st.columns(3)
    
    # Create a column for each player with their most up-to-date handicap
    for idx, name in enumerate(names):
        if idx % 3 == 0:
            with col1:
                
                # Find the most recent value of "handicap" for the current name
                recent_handicap = st.session_state.df.loc[st.session_state.df['name'] == name, 'handicap'].iloc[-1]
    
                # Display that player's handicap
                st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="font-size:35px; color: orange;">{name}</h2>
                <h2 style="font-size:30px; color: #40a3ff;">{recent_handicap:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
                st.markdown("---")
                
        elif idx % 3 == 1:
            with col2:
                # Find the most recent value of "handicap" for the current name
                recent_handicap = st.session_state.df.loc[st.session_state.df['name'] == name, 'handicap'].iloc[-1]
    
                # Display that player's handicap
                st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="font-size:35px; color: orange;">{name}</h2>
                <h2 style="font-size:30px; color: #40a3ff;">{recent_handicap:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
                st.markdown("---")

        else:
            with col3:
                # Find the most recent value of "handicap" for the current name
                recent_handicap = st.session_state.df.loc[st.session_state.df['name'] == name, 'handicap'].iloc[-1]
    
                # Display that player's handicap
                st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="font-size:35px; color: orange;">{name}</h2>
                <h2 style="font-size:30px; color: #40a3ff;">{recent_handicap:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
                st.markdown("---")
        

    # Trends, line plots
    # st.markdown("---")
    st.subheader(":violet[Trends Over Time:]")
    st.write("Use the dropdown menu to select a metric and the date slider to select a range of dates")
    trend_var = st.selectbox("Trend Metric:", [*reverse_labels.keys()], index=7)
    trend_data = st.session_state.df.dropna(subset=reverse_labels[trend_var])

    # Set up min and max dates
    min_date = trend_data['date'].min().date()
    max_date = trend_data['date'].max().date()
    
    # Use st.date_input to select start and end dates
    start_date, end_date = st.slider("Date Range", min_value = min_date, max_value=max_date, \
                        value=(min_date, max_date), format="YYYY-MM-DD")
    
    # Line plot of all data with time slider to choose time window
    st.plotly_chart(plot_statistics(data=trend_data.loc[(trend_data["date"] >= pd.to_datetime(start_date)) & (trend_data["date"] <= pd.to_datetime(end_date))], column = reverse_labels[trend_var], color_map=color_map))

    # Rolling averages to evaluate smoothed trends
    st.subheader(":violet[Rolling average statistics:]")
    st.write("Use the dropdown menu to select a metric and the slider to select the size of your window")
    roll_var = st.selectbox("Rolling Average Metric:", [*reverse_labels.keys()], index=0)
    window = st.slider("Number of Rounds to Include in the Rolling Window:", min_value=5, max_value = 30) 
    st.plotly_chart(rolling_avg(st.session_state.df, reverse_labels[roll_var], window, color_map=color_map))

    # Mean, median, stddev aggregate stats for different metrics
    st.subheader(":violet[Average, median, and standard deviation aggregate statistics:]")
    st.write("Use the dropdown menu to select a metric")
    agg_var = st.selectbox("Aggregate Metric:", [*reverse_labels.keys()], index=0)
    st.plotly_chart(mean_med_stats(st.session_state.df, reverse_labels[agg_var]))

    # Distribution plots for various metrics
    st.subheader(":violet[Distributions: Comparing distributions of different statistics across players:]")
    st.write("Use the dropdown menu to select a metric")
    hist_var = st.selectbox("Distribution Metric:", [*reverse_labels.keys()], index=0)
    st.plotly_chart(histplot(st.session_state.df, reverse_labels[hist_var], color_map=color_map))

    # Proportion pie charts
    st.subheader(":violet[Proportions of contributing statistics:]")
    st.write("Use the dropdown menu to select a metric")

    pie_var = st.selectbox("Proportion Metric:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index"]], index=1)
    cols = st.columns([1 for i in names])
    for idx, name in enumerate(names):
        with cols[idx]:
            st.plotly_chart(pie_chart(st.session_state.df, reverse_labels[pie_var], name))


    # Scatter plots of adj_gross_score vs other numeric variables with size option
    st.subheader(":violet[Adjusted Gross Score vs Contributing Statistics:]")
    st.write("Use the first dropdown menu to select a metric for the X-Axis and the second dropdown to optionally add a 'size' metric")
    
    scatter_var = st.selectbox("X-Variable:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index"]], index=0)
    
    size_var = st.selectbox("Size-Variable (Optional):", [None] + [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index"]], index=0)
    
    
    st.plotly_chart(scatter(data=st.session_state.df, column=reverse_labels[scatter_var], size=reverse_labels[size_var] if size_var else None, color_map=color_map)) 


    # Correlation analysis of the above scatterplot
    st.subheader(":violet[Feature Correlation:]")
    
    corr = st.session_state.df[["adj_gross_score", reverse_labels[scatter_var]]].corr().iloc[0,1]
    
    st.write(f'Overall Pearson Correlation for :blue[_Adjusted Gross Score and {scatter_var}_]: :green[**{corr:.3f}**]')

    # Boilerplate analysis options
    if abs(corr) <.4:
        # Weak correlation
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a weak correlation, and therefore it is likely that this statistic is not significantly influencing your scores.")
    
    # Positive correlation
    elif .7 > corr >= .4:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a moderate positive correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will also increase and vice versa.")
    elif corr > .7:
        
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a strong positive correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will also increase and vice versa.")
    
    # Negative correlation
    elif -.7 < corr <= -.4:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a moderate negative correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will decrease and vice versa.")
    elif corr < -.7:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a strong negative correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will decrease and vice versa.")

    # Player-by-player correlations
    st.write("Player by Player Correlation Breakdown for Comparison:")

    st.dataframe(st.session_state.df.groupby("name")[["adj_gross_score", reverse_labels[scatter_var]]].corr().reset_index()\
            .rename(columns={reverse_labels[scatter_var]:"Correlation", "name":"Player Name"})\
                 .loc[::2,["Player Name", "Correlation"]], hide_index=True)

    
    # Search for a specific date's records
    st.subheader(":violet[Search for a Specific Round:]")

    min_search_date = st.session_state.df['date'].min().date()
    max_search_date = st.session_state.df['date'].max().date()
    st.write("Use the first dropdown menu to select a date to search, then select an individual player for a graph of their data")
    round_date = st.date_input("Choose a Date to Search:", min_value=min_search_date, max_value=max_search_date, value=None)
    
    query_df = st.session_state.df.loc[st.session_state.df["date"] == pd.to_datetime(round_date)]
    if query_df.empty:
        st.subheader(":red[No records found for this date]")
    
    if not query_df.empty:         #### Edit Later #### 
        st.dataframe(query_df[["name"]+[key for key in label_dict.keys() if key not in ['birdies', 'dbl_bogeys_plus', 'profit/loss']]].rename(columns=label_dict).rename(columns={"name":"Player"})\
                     .drop(columns="Handicap Index"), hide_index=True, use_container_width=True)
        for name in query_df["name"].unique():
            st.plotly_chart(find_round(query_df, name, pd.to_datetime(round_date, format='YYYY-MM-dd')))
    
    
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