import pandas as pd
import numpy as np
import streamlit as st

def background_info():
    """
    Displays the text and background information for this project
    """

    
    # Body Paragraphs
    st.subheader(":blue[Project Background]")
    
    st.markdown("""Are your "friends" like mine, always negotiating in bad faith to get favorable lines on the 1st tee box? This project was born from that very frustration. The solution: verified player handicaps. There are barriers for the casual golfer to acquire a verified handicap.""")
    
    st.markdown("""The USGA (United States Golf Association) says that "...in order to establish and maintain a Handicap Index, a player must be a member of an authorized golf club." There are mobile applications that offer the ability to track golf statistics and calculate a handicap, but those apps often have associated subscription fees. Furthermore, if the members of my regular golf group don't want to use the app or pay the subscription, then their handicaps will continue to be unknown values.""")
    
    # Paragraph 2
    st.subheader(":blue[Calculating Player Handicaps]")
    st.markdown("""To calculate player handicaps, the "handicap differential" for _each round_ is recorded. The handicap differential is calculated:""")

    # Equation for Handicap Differential
    st.markdown(r"""
$$
\text{Handicap Differential} = \frac{(\text{Adjusted Gross Score} - \text{Course Rating}) \times 113}{\text{Slope Rating}}
$$
""")

    # Bullet Points for Components of the Equation
    st.markdown("""Where:
    
- Adjusted Gross Score (AGS): The score you actually shot, adjusted for equitable stroke control (ESC).
- Course Rating: A number representing the difficulty of a course for a scratch golfer.
- Slope Rating: A number representing the difficulty of a course for a bogey golfer compared to a scratch golfer. 
- The standard Slope Rating is 113.""")

    # Equitable Stroke Control Paragraph
    st.markdown("""_Equitable stroke control_ means that for a given handicap, there is a maximum allowable score on any individual hole. _"ESC"_ helps to protect a golfer's handicap from any individual hole where they play uncharacteristically bad golf. Those maximum scores for individual holes are capped as follows:""")
    
    # DF display
    st.dataframe(pd.read_csv("ESC.csv").rename(columns={"Course Handicap":"Player Handicap"}), use_container_width=True, hide_index=True)

    
    # Handicap Calc Paragraph
    st.markdown("""As you continue to record the handicap differentials for each round played, you will also need to meet a minimum threshold for rounds played. An official handicap can be obtained after recording 54 holes of golf. Your handicap will be calculated by averaging a certain number of your lowest scores depending on how many rounds you have recorded.""")

    # Df display
    st.dataframe(pd.read_csv("handicap_rds.csv", dtype={"Adjustment":str}).rename(columns={"Differentials to Use":"Differential Scores to Use",
                                                                "Adjustment":"Handicap Adjustment"}), use_container_width=True, hide_index=True)

    # Conclusion
    st.markdown("""Finally, you can find your handicap by applying this calculation:""")

    
    # Handicap Index Equation
    st.markdown(r"""
$$
\text{Handicap Index} = (\text{Average of Lowest Differentials} \times 0.96) + \text{Adjustment}
$$
""")

    
    # Synthetic Data Display
    st.markdown("---")

    st.subheader(":blue[While my friends and I collect some data...]")
    st.markdown("""I have generated some synthetic data to demonstrate the visualizations we will use to track and analyze our scores. This data is purely for purposes of demonstration, and some of the statistics and relationships shown will likely not reflect reality for most golfers. \n \nThat being said, I am still the best golfer based on synthetic data......""")

    st.markdown(":blue[_A brief note about the plots:_]")
    st.markdown("You can isolate a plot component by double-clicking on it in the legend, or you can toggle on/off individual plot items by clicking on the desired item in the legend. You can also click and drag over quadrants of graphs to zoom in on areas of interest. Click the home icon in the upper-right corner or double-click on the plot to zoom back out to the original scope. Finally, as you move your mouse cursor over the plots, you will notice hover-values that display additional information. Thank you and enjoy the dashboard")
    
    st.markdown("---")