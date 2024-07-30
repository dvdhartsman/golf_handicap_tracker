import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
from utils import add_round, get_handicaps, fill_handicaps, plot_statistics, histplot, pie_chart, dist_plot, rolling_avg, scatter, mean_med_stats, find_round, handicap_differentials, total_profit, agg_features_by_cat, add_border


def dashboard(data):
    """
    Display plots and input options for the simulated data
    """

    # Data load
    if "df" not in st.session_state:
        data = pd.read_csv("synthetic_data.csv", parse_dates=["date"])   

    # Colors for plots to avoid repeating colors
    color_map = dict(zip([name for name in data["name"].unique()], px.colors.qualitative.Vivid))


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
        "opponent/s":"Opponent/s",
        "notes":"Notes"
    }

    # Also useful for labeling, titling, etc.
    reverse_labels = {val:key for key, val in label_dict.items()}

    # Numerical Features
    num_names = ["putts", "3_putts", "fairways_hit", "gir", "penalty/ob", "birdies", "trpl_bogeys_plus", "adj_gross_score", "profit/loss"]
    cat_names = ["golf_course", "match_format", "opponent/s"]

    num_features = [label_dict[i] for i in num_names]
    cat_features = [label_dict[j] for j in cat_names]


    # ------------------- Beginning of Plot Section ------------------------------


 # -------------------- # Synthetic Data Display ----------------------   
    
    # add_border()
    # Numerical handicap displays for each player #ff2400 #f94d00
    st.markdown("""<div style="text-align: center; font-size:45px; color:orange">  
            <b><u><i>Up-To-Date Player Handicaps:</i></u></b>
            </div>""", unsafe_allow_html=True)
    
    # finding unique players with valid handicaps
    names = data.dropna(subset="handicap")["name"].unique()
    col1, col2, col3 = st.columns(3)
    
    # Create a column for each player with their most up-to-date handicap
    for idx, name in enumerate(names):
        if idx % 3 == 0:
            with col1:
                
                # Find the most recent value of "handicap" for the current name
                recent_handicap = data.loc[data['name'] == name, 'handicap'].iloc[-1]
    
                # Display that player's handicap
                st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="font-size:35px; color: #40a3ff;">{name}</h2>
                <h2 style="font-size:30px; color: #cc0000;">{recent_handicap:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
                st.markdown("""<hr style="border: 2px solid #e5e4e2">""", unsafe_allow_html=True)
                
        elif idx % 3 == 1:
            with col2:
                # Find the most recent value of "handicap" for the current name
                recent_handicap = data.loc[data['name'] == name, 'handicap'].iloc[-1]
    
                # Display that player's handicap
                st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="font-size:35px; color: #40a3ff;">{name}</h2>
                <h2 style="font-size:30px; color: #cc0000;">{recent_handicap:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
                st.markdown("""<hr style="border: 2px solid #e5e4e2">""", unsafe_allow_html=True)

        else:
            with col3:
                # Find the most recent value of "handicap" for the current name
                recent_handicap = data.loc[data['name'] == name, 'handicap'].iloc[-1]
    
                # Display that player's handicap
                st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="font-size:35px; color: #40a3ff;">{name}</h2>
                <h2 style="font-size:30px; color: #cc0000;">{recent_handicap:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
                st.markdown("""<hr style="border: 2px solid #e5e4e2">""", unsafe_allow_html=True)
        


    # PROFIT AND LOSS
    add_border()
    devil_emoji = "\U0001F608"
    st.subheader(":blue[Overall Profit/Loss:]")
    st.plotly_chart(total_profit(data, color_map=color_map))

    add_border()
    
    # Aggregation of stats by different categories
    st.subheader(":blue[Aggregate statistics by category:]")
    
    # For labels
    agg_dict = {
        "mean":"Average Value",
        "median":"Median Value",
        "sum":"Sum/Total"
    }

    # Also for labels
    agg_dict_rev = {val:key for key, val in agg_dict.items()}
    
    
    # Selection options
    agg_feat = st.selectbox("Choose a metric to aggregate:", num_features, index=8)
    agg_cat = st.selectbox("Choose a category to group by:", cat_features)
    agg_func = st.selectbox("What measure would you like to use?", [*agg_dict_rev.keys()])
    
    # Plot 
    st.plotly_chart(agg_features_by_cat(data=data, category=reverse_labels[agg_cat], 
                                        feature=reverse_labels[agg_feat], aggfunc=agg_dict_rev[agg_func]))
    
    add_border()
    
    # Trends, line plots
    st.subheader(":blue[Trends Over Time:]")
    st.write("Use the dropdown menu to select a metric and the date slider to select a range of dates")
    
    trend_var = st.selectbox("Trend Metric:", num_features, index=7)
    trend_data = data.dropna(subset=reverse_labels[trend_var])

    # Set up min and max dates
    min_date = trend_data['date'].min().date() 
    max_date = trend_data['date'].max().date() + pd.Timedelta(days=1)
    
    # Use st.date_input to select start and end dates
    start_date, end_date = st.slider("Date Range", min_value = min_date, max_value=max_date, \
                        value=(min_date, max_date), format="YYYY-MM-DD")
    
    # Line plot of all data with time slider to choose time window
    st.plotly_chart(plot_statistics(data=trend_data.loc[(trend_data["date"] >= pd.to_datetime(start_date)) & (trend_data["date"] <= pd.to_datetime(end_date))], column = reverse_labels[trend_var], color_map=color_map))
    add_border()

    # Rolling averages to evaluate smoothed trends
    st.subheader(":blue[Rolling average statistics:]")
    st.write("Use the dropdown menu to select a metric and the slider to select the size of your window")
    roll_var = st.selectbox("Rolling Average Metric:", num_features, index=0)
    window = st.slider("Number of Rounds to Include in the Rolling Window:", min_value=5, max_value = 30) 
    st.plotly_chart(rolling_avg(data, reverse_labels[roll_var], window, color_map=color_map))
    add_border()

    # Mean, median, stddev aggregate stats for different metrics
    st.subheader(":blue[Average, median, and standard deviation aggregate statistics:]")
    st.write("Use the dropdown menu to select a metric")
    agg_var = st.selectbox("Aggregated Metric:", num_features, index=0)
    st.plotly_chart(mean_med_stats(data, reverse_labels[agg_var]))
    add_border()

    # Distribution plots for various metrics
    st.subheader(":blue[Distributions: Comparing distributions of different statistics across players:]")
    st.write("Use the dropdown menu to select a metric")
    hist_var = st.selectbox("Distribution Metric:", num_features, index=0)
    st.plotly_chart(histplot(data, reverse_labels[hist_var], color_map=color_map))
    add_border()

    # Proportion pie charts
    st.subheader(":blue[Proportions of contributing statistics:]")
    st.write("Use the dropdown menu to select a metric")

    # "Profit/Loss", "Match Format", "Opponent/s", "Golf Course",
    pie_var = st.selectbox("Proportion Metric:", 
                           [key for key in reverse_labels.keys() if key not in ["Adjusted Gross Score", "Handicap Differential", 
                                                                                "Handicap Index",  "Notes"]], index=1)
    
    
    names_list = data.dropna(subset=reverse_labels[pie_var])["name"].unique()
    col1, col2, col3 = st.columns(3)
    
    # Create a column for each player with their most up-to-date handicap
    for idx, name in enumerate(names_list):
        if idx % 3 == 0:
            with col1:
                
                st.plotly_chart(pie_chart(data, reverse_labels[pie_var], name))
                st.markdown("---")
                
        elif idx % 3 == 1:
            with col2:
                st.plotly_chart(pie_chart(data, reverse_labels[pie_var], name))
                st.markdown("---")
                

        else:
            with col3:
                st.plotly_chart(pie_chart(data, reverse_labels[pie_var], name))
                st.markdown("---")


    # Scatter plots of adj_gross_score vs other numeric variables with size option
    add_border()
    st.subheader(":blue[Adjusted Gross Score vs Selected Metrics:]")
    st.write("Use the first dropdown menu to select a metric for the X-Axis and the second dropdown to optionally add a 'size' metric")
    
    scatter_var = st.selectbox("X-Variable:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index", "Match Format",
                                                  "Opponent/s", "Golf Course", "Notes"]], index=0)
    
    size_var = st.selectbox("Size-Variable (Optional):", [None] + [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index", "Match Format",
                                                  "Opponent/s", "Golf Course", "Notes", "Profit/Loss"]], index=0)
    
    
    st.plotly_chart(scatter(data=data, column=reverse_labels[scatter_var], size=reverse_labels[size_var] if size_var else None, color_map=color_map))
    add_border()


    # Correlation analysis of the above scatterplot
    st.subheader(":blue[Feature Correlation:]")
    
    corr = data[["adj_gross_score", reverse_labels[scatter_var]]].corr().iloc[0,1]
    
    st.write(f'Overall Pearson Correlation for :orange[_Adjusted Gross Score_] and :orange[_{scatter_var}_]: :green[**{corr:.3f}**]')

    # Boilerplate analysis options
    if abs(corr) <.3:
        # Weak correlation
        st.write(f"The relationship between :orange[Adjusted Gross Score] and :orange[{scatter_var}] demonstrates a :orange[_weak correlation_], and therefore it is likely that this statistic is not significantly influencing your scores.")
    
    # Positive correlation
    elif .7 > corr >= .3:
        st.write(f"The relationship between :orange[Adjusted Gross Score] and :orange[{scatter_var}] demonstrates a :blue[_moderate positive_] correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will also increase and vice versa.")
    elif corr > .7:
        
        st.write(f"The relationship between :orange[Adjusted Gross Score] and :orange[{scatter_var}] demonstrates a :green[_strong positive correlation_], meaning that as {scatter_var} increases, Adjusted Gross Score will also increase and vice versa.")
    
    # Negative correlation
    elif -.7 < corr <= -.3:
        st.write(f"The relationship between :orange[Adjusted Gross Score] and :orange[{scatter_var}] demonstrates a :blue[_moderate negative correlation_], meaning that as {scatter_var} increases, Adjusted Gross Score will decrease and vice versa.")
    elif corr < -.7:
        st.write(f"The relationship between :orange[Adjusted Gross Score] and :orange[{scatter_var}] demonstrates a :red[_strong negative correlation_], meaning that as {scatter_var} increases, Adjusted Gross Score will decrease and vice versa.")
    add_border()

    # Player-by-player correlations
    st.write("Player by Player Correlation Breakdown for Comparison:")

    st.dataframe(data.groupby("name")[["adj_gross_score", reverse_labels[scatter_var]]].corr().reset_index()\
            .rename(columns={reverse_labels[scatter_var]:"Correlation", "name":"Player Name"})\
                 .loc[::2,["Player Name", "Correlation"]], hide_index=True)
    add_border()

    
    # Search for a specific date's records
    st.subheader(":blue[Search for a Specific Round:]")

    min_search_date = data['date'].min().date()
    max_search_date = data['date'].max().date()
    st.write("Use the first dropdown menu to select a date to search, then select an individual player for a graph of their data from that date")
    round_date = st.date_input("Choose a Date to Search:", min_value=min_search_date, max_value=max_search_date, value=None)
    
    query_df = data.loc[data["date"] == pd.to_datetime(round_date)]
    if query_df.empty:
        st.subheader(":red[No records found for this date]")
    
    if not query_df.empty:         #### Edit Later #### 
        st.dataframe(query_df.drop(columns=["jittered_col", "notes", "handicap"]).rename(columns=label_dict)\
                     .rename(columns={"name":"Player", "date":"Date", "course_rating":"Course Rating", "slope_rating":"Slope Rating"}),\
                     hide_index=True, use_container_width=True)
        add_border()
        for name in query_df["name"].unique():
            st.plotly_chart(find_round(query_df, name, pd.to_datetime(round_date, format='YYYY-MM-dd')))
            add_border()