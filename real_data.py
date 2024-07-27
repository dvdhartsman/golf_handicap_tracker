import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
from utils import add_round, get_handicaps, fill_handicaps, plot_statistics, histplot, pie_chart, dist_plot, rolling_avg, scatter, mean_med_stats, find_round, handicap_differentials, total_profit, profit_by_match_type


def real_data():
    """
    display analysis for real data
    """

    df = pd.read_csv("real_data.csv", parse_dates=["date"])

    # Colors for plots to avoid repeating colors
    color_map = dict(zip([name for name in df["name"].unique()], px.colors.qualitative.Vivid))


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
        "trpl_bogeys_plus":"Triple Bogey+",
        "profit/loss":"Profit/Loss",
        "match_format":"Match Format",
        "golf_course":"Golf Course",
        "opponent_s":"Opponent/s",
        "notes":"Notes"
    }

    # Also useful for labeling, titling, etc.
    reverse_labels = {val:key for key, val in label_dict.items()}
    
    
# --------------------------------- Displayed Info ---------------------------------- 
    # Numerical handicap displays for each player
    st.markdown("""<div style="text-align: center; font-size:40px; color:gold">
            <b><u><i>Current Player Handicaps:</i></u></b>
            </div>""", unsafe_allow_html=True)
    
    # finding unique players with valid handicaps
    names = df.dropna(subset="handicap")["name"].unique()
    col1, col2, col3 = st.columns(3)
    
    # Create a column for each player with their most up-to-date handicap
    for idx, name in enumerate(names):
        if idx % 3 == 0:
            with col1:
                
                # Find the most recent value of "handicap" for the current name
                recent_handicap = df.loc[df['name'] == name, 'handicap'].iloc[-1]
    
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
                recent_handicap = df.loc[df['name'] == name, 'handicap'].iloc[-1]
    
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
                recent_handicap = df.loc[df['name'] == name, 'handicap'].iloc[-1]
    
                # Display that player's handicap
                st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="font-size:35px; color: orange;">{name}</h2>
                <h2 style="font-size:30px; color: #40a3ff;">{recent_handicap:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
                st.markdown("---")

    
    # st.markdown("---")

    # PROFIT AND LOSS

    st.subheader(":violet[The only reason we play, Profit and Loss:]")
    st.plotly_chart(total_profit(df, color_map=color_map))

    agg_dict = {
        "mean":"Average Profit/Loss",
        "median":"Median Profit/Loss",
        "sum":"Total Profit/Loss"
    }

    agg_dict_rev = {val:key for key, val in agg_dict.items()}
    
    agg_func = st.selectbox("Profit and Loss by Match Format: How would you like to Aggregate?", [*agg_dict_rev.keys()])
    st.plotly_chart(profit_by_match_type(df, agg_dict_rev[agg_func]))
    
    
    # Trends, line plots
    st.subheader(":violet[Trends Over Time:]")
    
    
    st.write("Use the dropdown menu to select a metric and the date slider to select a range of dates")
    trend_var = st.selectbox("Trend Metric:", [key for key in reverse_labels.keys() if key != "Match Format"], index=7)
    trend_data = df.dropna(subset=reverse_labels[trend_var])

    # Set up min and max dates
    min_date = (trend_data['date'].min() - pd.Timedelta(days=1)).date()
    max_date = (trend_data['date'].max() + pd.Timedelta(days=1)).date()
    st.write(min_date, max_date)
    
    # Use st.date_input to select start and end dates
    start_date, end_date = st.slider("Date Range", min_value = min_date, max_value=max_date, \
                        value=(min_date, max_date), format="YYYY-MM-DD")
    
    # Line plot of all data with time slider to choose time window
    st.plotly_chart(plot_statistics(data=trend_data.loc[(trend_data["date"] >= pd.to_datetime(start_date)) & (trend_data["date"] <= pd.to_datetime(end_date))], column = reverse_labels[trend_var], color_map=color_map))

    # Rolling averages to evaluate smoothed trends
    st.subheader(":violet[Rolling average statistics:]")
    st.write("Use the dropdown menu to select a metric and the slider to select the size of your window")
    roll_var = st.selectbox("Rolling Average Metric:", [key for key in reverse_labels.keys() if key != "Match Format"], index=0)
    window = st.slider("Number of Rounds to Include in the Rolling Window:", min_value=5, max_value = 30) 
    st.plotly_chart(rolling_avg(df, reverse_labels[roll_var], window, color_map=color_map))

    # Mean, median, stddev aggregate stats for different metrics
    st.subheader(":violet[Average, median, and standard deviation aggregate statistics:]")
    st.write("Use the dropdown menu to select a metric")
    agg_var = st.selectbox("Aggregate Metric:", [key for key in reverse_labels.keys() if key != "Match Format"], index=0)
    st.plotly_chart(mean_med_stats(df, reverse_labels[agg_var]))

    # Distribution plots for various metrics
    st.subheader(":violet[Distributions: Comparing distributions of different statistics across players:]")
    st.write("Use the dropdown menu to select a metric")
    hist_var = st.selectbox("Distribution Metric:", [key for key in reverse_labels.keys() if key != "Match Format"], index=0)
    st.plotly_chart(histplot(df, reverse_labels[hist_var], color_map=color_map))

    # Proportion pie charts
    st.subheader(":violet[Proportions of contributing statistics:]")
    st.write("Use the dropdown menu to select a metric")

    pie_var = st.selectbox("Proportion Metric:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index", "Match Format"]], index=1)
    cols = st.columns([1 for i in names])
    for idx, name in enumerate(names):
        with cols[idx]:
            st.plotly_chart(pie_chart(df, reverse_labels[pie_var], name))


    # Scatter plots of adj_gross_score vs other numeric variables with size option
    st.subheader(":violet[Adjusted Gross Score vs Contributing Statistics:]")
    st.write("Use the first dropdown menu to select a metric for the X-Axis and the second dropdown to optionally add a 'size' metric")
    
    scatter_var = st.selectbox("X-Variable:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index", "Match Format"]], index=0)
    
    size_var = st.selectbox("Size-Variable (Optional):", [None] + [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index", "Match Format"]], index=0)
    
    
    st.plotly_chart(scatter(data=df, column=reverse_labels[scatter_var], size=reverse_labels[size_var] if size_var else None, color_map=color_map)) 


    # Correlation analysis of the above scatterplot
    st.subheader(":violet[Feature Correlation:]")
    
    corr = df[["adj_gross_score", reverse_labels[scatter_var]]].corr().iloc[0,1]
    
    st.write(f'Overall Pearson Correlation for :blue[_Adjusted Gross Score_] and :blue[{scatter_var}_]: :green[**{corr:.3f}**]')

    # Boilerplate analysis options
    if abs(corr) <.3:
        # Weak correlation
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a weak correlation, and therefore it is likely that this statistic is not significantly influencing your scores.")
    
    # Positive correlation
    elif .7 > corr >= .3:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a moderate positive correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will also increase and vice versa.")
    elif corr > .7:
        
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a strong positive correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will also increase and vice versa.")
    
    # Negative correlation
    elif -.7 < corr <= -.3:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a moderate negative correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will decrease and vice versa.")
    elif corr < -.7:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a strong negative correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will decrease and vice versa.")

    # Player-by-player correlations
    st.write("Player by Player Correlation Breakdown for Comparison:")

    st.dataframe(df.groupby("name")[["adj_gross_score", reverse_labels[scatter_var]]].corr().reset_index()\
            .rename(columns={reverse_labels[scatter_var]:"Correlation", "name":"Player Name"})\
                 .loc[::2,["Player Name", "Correlation"]], hide_index=True)

    
    # Search for a specific date's records
    st.subheader(":violet[Search for a Specific Round:]")

    min_search_date = df['date'].min().date()
    max_search_date = df['date'].max().date()
    st.write("Use the first dropdown menu to select a date to search, then select an individual player for a graph of their data")
    round_date = st.date_input("Choose a Date to Search:", min_value=min_search_date, max_value=max_search_date, value=None)
    
    query_df = df.loc[df["date"] == pd.to_datetime(round_date)]
    if query_df.empty:
        st.subheader(":red[No records found for this date]")
    
    if not query_df.empty:         #### Edit Later #### 
        st.dataframe(query_df[["name"]+[key for key in label_dict.keys()]].rename(columns=label_dict).rename(columns={"name":"Player"})\
                     .drop(columns="Handicap Index"), hide_index=True, use_container_width=True)
        for name in query_df["name"].unique():
            st.plotly_chart(find_round(query_df, name, pd.to_datetime(round_date, format='YYYY-MM-dd')))