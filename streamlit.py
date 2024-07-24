import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st

from utils import add_round, get_handicap, fill_handicaps, plot_statistics, histplot, pie_chart, dist_plot, rolling_avg, scatter, mean_med_stats

def main():

    st.set_page_config(page_title="Golf Group Handicap Tracker",
                   page_icon=':golf:',
                      layout="wide")
    
    st.title(':orange[Golf Group Handicap Tracker]')
    st.subheader(":blue[_Statistics to Inform and Expedite Match Negotiations_]")
    st.markdown("---")

    st.subheader(":green[Motivation]")
    st.markdown("""Are your "friends" like mine, always negotiating in bad faith to get favorable lines on the 1st tee box? This project was born from that very frustration. The solution: verified player handicaps. There are barriers for the casual golfer to acquire a verified handicap.""")
    st.markdown("""The USGA (United States Golf Association) says that "...in order to establish and maintain a Handicap Index, a player must be a member of an authorized golf club." There are mobile applications that offer the ability to track golf statistics and calculate a handicap, but those apps often have associated subscription fees. Furthermore, if the members of my regular golf group don't want to use the app or pay the subscription, then their handicaps will continue to be unknown values.""")
    
    st.subheader(":green[Get Your Own Handicap]")
    st.markdown("""My app allows me to generate and track the handicaps for the members of my golf circle. To calculate handicaps, the "handicap differential" for _each round_ is recorded. The handicap differential is calculated:""")

    st.markdown(r"""
$$
\text{Handicap Differential} = \frac{(\text{Adjusted Gross Score} - \text{Course Rating}) \times 113}{\text{Slope Rating}}
$$
""")

    st.markdown("""Where:
    
- Adjusted Gross Score (AGS): The score you actually shot, adjusted for equitable stroke control (ESC).
- Course Rating: A number representing the difficulty of a course for a scratch golfer.
- Slope Rating: A number representing the difficulty of a course for a bogey golfer compared to a scratch golfer. 
- The standard Slope Rating is 113.""")

    st.markdown("""_Equitable stroke control_ means that for a given handicap, there is a maximum value on any individual hole. ESC helps protect a golfer's handicap from being unduly impacted by any individual hole where they play uncharacteristically bad golf. Those maximum values are as follows:""")
    st.dataframe(pd.read_csv("ESC.csv"), use_container_width=True, hide_index=True)

    st.markdown("""As you continue to record the handicap differentials for each round played, you will also need to meet a minimum threshold for rounds played. An official handicap can be obtained after recording 54 holes of golf. Your handicap will be calculated by averaging a certain number of your lowest scores depending on how many rounds you have recorded.""")

    st.dataframe(pd.read_csv("handicap_rds.csv"), use_container_width=True, hide_index=True)

    st.markdown("""Finally, you can find your handicap by applying this calculation:""")

    st.markdown(r"""
$$
\text{Handicap Index} = (\text{Average of Lowest Differentials} \times 0.96) + \text{Adjustment}
$$
""")

    st.markdown("---")

    st.subheader("While my friends and I collect some data...")
    st.markdown("""I have generated some synthetic data to demonstrate the visualizations we will use to track and analyze our scores:""")
    

    df = pd.read_csv("synthetic_data.csv", parse_dates=["date"]).sort_values(by="date")

    st.markdown("""<div style="text-align: center; font-size:40px; color:lightblue">
            <b><u>Current Handicaps:</u></b>
            </div>""", unsafe_allow_html=True)
    names = df["name"].unique()
    cols = st.columns([1 for i in names])
    
    for idx, name in enumerate(names):
        with cols[idx]:
            # Find the most recent value of "twentyRd_handicap" for the current name
            recent_handicap = df.loc[df['name'] == name, 'twentyRd_handicap'].iloc[-1]
            # st.metric(label=f"{name}", value=recent_handicap.round(3))
            st.markdown(f"""
        <div style="text-align: center;">
            <h2 style="font-size:35px; color: orange;">{name}</h2>
            <h2 style="font-size:30px; color: green;">{recent_handicap:.4f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    # Set up min and max dates
    min_date = df['date'].min()
    max_date = df['date'].max()
    
    # Use st.date_input to select start and end dates
    start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
    
    st.plotly_chart(plot_statistics(df.loc[(df["date"] >= min_date) & (df["date"] <= max_date)], "twentyRd_handicap"))

    st.plotly_chart(histplot(df, "adj_gross_score"))

    cols = st.columns([1 for i in names])
    for idx, name in enumerate(names):
        with cols[idx]:
            st.plotly_chart(pie_chart(df, "gir", name))

    st.plotly_chart(mean_med_stats(df, "gir"))

    st.plotly_chart(rolling_avg(df, "adj_gross_score", 20))



if __name__ == "__main__":
    main()