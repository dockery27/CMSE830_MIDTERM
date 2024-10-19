# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 21:19:34 2024

@author: docke
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import altair as alt

df = pd.read_csv("combined_data.csv")
df.drop(columns=["Unnamed: 0",],axis=1,inplace=True) # this is an extra index column
df_no_unc = df.drop(columns=["radius_unc", "MASS EXCESS UNC", "BINDING ENERGY UNC", "ATOMIC MASS UNC"],axis=1)

df_no_unc_subset = df_no_unc[["radius_val","MASS EXCESS","BINDING ENERGY/A", "ATOMIC MASS", " half_life [s]"]]
df_no_unc_subset[" half_life [s]"] = np.log(df_no_unc_subset[" half_life [s]"]) # make log scale due to variation in values
scaler = StandardScaler()
scaler.fit(df_no_unc_subset)
standardized = scaler.transform(df_no_unc_subset)
df_scaled = pd.DataFrame(standardized,columns=["radius_val","MASS EXCESS","BINDING ENERGY/A", "ATOMIC MASS", " half_life [s]"])
df_scaled = pd.concat([df_scaled, df_no_unc[['z', 'n', 'a', 'N-Z', ' jp', ' decay', 'radioactive']]], axis=1)

df_scaled_lowmass = df_scaled[df_scaled["n"] >= 18]
df_scaled_lowmass = df_scaled_lowmass[df_scaled_lowmass["n"] <= 30]

st.title("Nuclear Charge Radius Exploration")
st.write('''
    Here we explore the relationship between nuclear charge radius and other properties 
    of the nucleus. The nuclear charge radius is a measure of the proton distribution in the 
    nucleus, which is a useful measure to test nuclear physics theory and the focus of my thesis 
    work. This project explores the connection between nuclear charge radius and nuclear 
    mass, decay mode, binding energy, and more.
    
    Data was compiled from the international atomic energy agency databases for charge radii, nuclear mass,
    and half lives. This process is explained in detail in the github. The relationship between the charge radius 
    and key features are shown in this work.
''')
tab1, tab2 = st.tabs(["Global Distribution", "Shell Closure"])

with tab1:
    st.write('''
        The nuclear charge radius (R) has a general trend that can be explained by the number of 
        protons and neutrons in the nucleus, which is referred to as the mass number (A).
    ''')
    st.latex("R = 1.2 A^{1/3}")
    st.write('''
        Modern nuclear physics research focuses on the local evolution of the charge radius, which 
        is explored in the other tab for a shell closure region . Here we look at this global 
        relationship with mass number as well as other key observables of the nucleus.
    ''')
    with st.expander("Mass Number"):
        st.write('''
                 The mass number refers to the number of protons and neutrons in the nucleus. This is 
                 an integer number, and in this dataset it varies from 1 to 248 with a median of 137.
        ''')
        chart = alt.Chart(df_scaled).mark_point().encode(
            x=alt.X('a', title="Mass Number"),
            y=alt.Y('radius_val', title="Charge Radius (z-scaled)"),
            color=' decay',
            tooltip=['a', 'radius_val', 'z', 'n', ' decay']
            ).interactive()
        st.altair_chart(chart)
        st.caption('''
                   The standard model taken for nuclear charge radius follows the trend in 
                   this figure. The color of the points refers to the mode of radioactive decay 
                   of the nucleus.
        ''')
    with st.expander("Radioactivity"):
        st.write('''
                 Nuclei can either be stable (do not decay) or radioactive (decay to a different nucleus). 
                 Here we see the effect of radioactivity on the nuclear charge radius.
        ''')
        fig = plt.figure(figsize=(6,6))
        sns.histplot(df_scaled,x="radius_val",hue="radioactive")
        plt.xlabel("Charge Radius (z-scaled)",fontsize="x-large")
        plt.ylabel("Count",fontsize="x-large")
        st.pyplot(plt)
        st.caption('''
                   A histrogram of the charge radii where the radioactive distribution (1) is 
                   compared to the stable distribution (0). The radioactive distribution extends to larger 
                   radii than the stable distribution, but there are no other major differences.
        ''')
    
    with st.expander("Decay Mode"):
        st.write('''
                 Radioactive nuceli can decay in a variety of pathways. In the below plot, the charge radii 
                 of different decay pathways is compared.
        ''')
        plt.figure(figsize=(8,4))
        sns.violinplot(df_scaled,x=" decay",y="radius_val")
        plt.xlabel("Decay Mode",fontsize="x-large")
        plt.ylabel("Charge Radius (z-scaled)",fontsize="x-large")
        st.pyplot(plt)
        st.caption('''
                   Each decay mode spans various radii distributions. Alpha and double beta-plus 
                   decay are confined to large radii. However, beta-minus and stable nuclei span much 
                   of the range of radii. Other decay modes span intermediate regions.
        ''')
    
    with st.expander("Mass Excess"):
        st.write('''
                 Mass excess is a measure of how much the nuclear mass deviates from the expected quantity 
                 for the mass number of the nucleus. Carbon-12 is taken as the standard mass value for computing 
                 mass excess.
        ''')
        chart2 = alt.Chart(df_scaled).mark_point().encode(
            x=alt.X('MASS EXCESS', title='Mass excess (z-scaled)'),
            y=alt.Y('radius_val', title='Charge Radius (z-scaled)'),
            color=' decay',
            tooltip=['MASS EXCESS', 'radius_val', 'z', 'n', ' decay', ]
            ).interactive()
        st.altair_chart(chart2)
        st.caption('''
                   Charge radii is plotted as a function of the mass excess value, which has been z-scaled. 
                   The charge radii roughly follow a rotated parabola relationship with the mass excess values.
        ''')
    
    
    with st.expander("Binding Energy per Nucleon"):
        st.write('''
                 Binding energy is a measure of how tighly bound individual nucleons are in the nucleus. Binding energy 
                 per nucleon peaks around the iron region of the nuclear chart and decreases at high and low masses.
        ''')
        chart3 = alt.Chart(df_scaled).mark_point().encode(
            x=alt.X('BINDING ENERGY/A', title="Binding enrgy per nucleon (z-scaled)"),
            y=alt.Y('radius_val', title='Charge radius (z-scaled)'),
            color=' decay',
            tooltip=['BINDING ENERGY/A', 'radius_val', 'z', 'n', ' decay']
            ).interactive()
        st.altair_chart(chart3)
        st.caption('''
                   Charge radii is plotted as a function of the binding energy per nucleon. The colors encode the decay 
                   method of the nucleus. An interesting trend is observed between the two variables which is hard to model 
                   mathematically.
        ''')
        
    st.write('''
        The above plots show that the standard global trend strongly correlates with the charge radius values. 
        Interestingly, trends are also observed between the decay mode, mass excess, and binding energy per nucleon. This 
        connection will be explored in future work to see if improved predictions can be generated as compared to the standard method.
    ''')
with tab2:
    st.write('''
             The local evolution of the nuclear charge radius deviates strongly from the general model and  is an active area of research. 
             It is of particular interest to benchmark 
             modern nuclear theories. One region of recent research is nuclear shell closures, which are configurations corresponding to 
             exceptionally stable nuclei analogous to noble gas valence shell closures in chemistry. Here we explroe the N=20 and N=28 neutron shell 
             closure region where recent experiments in the field have been focused.
             ''')
    st.header("Neutron Number")
    st.write('''
             Around shell closures the charge radius evolution includes many unique features. This includes 
             odd-even staggering of element chains with respect to neutron number and a reduction in the charge radius at shell closures. 
    ''')
    chart = alt.Chart(df_scaled_lowmass).mark_point().encode(
        x=alt.X('n', title="Neutron Number"),
        y=alt.Y('radius_val', title="Charge Radius (z-scaled)"),
        color='z:N',
        tooltip=['n', 'radius_val', 'z', 'a', ' decay']
        ).interactive()
    st.altair_chart(chart)
    st.caption('''
               The evolution of charge radius with respect to neutron number is plotted. Different 
               element chains are highlighted in different colors. Notably, the N=28 shell closure exhibits a 
               kink (reduction in radius) which is not seen in the N=20 shell closure. In addition, many element 
               chains have an odd-even stagger including calcium (Z=20)
    ''')
        
    with st.expander("Mass Number"):

        chart = alt.Chart(df_scaled_lowmass).mark_point().encode(
            x=alt.X('a', title="Mass Number"),
            y=alt.Y('radius_val', title="Charge Radius (z-scaled)"),
            color='z:N',
            tooltip=['a', 'radius_val', 'z', 'n', ' decay']
            ).interactive()
        st.altair_chart(chart)
        st.caption('''
                   The evolution of charge radius with respect to  mass number is plotted. While a trend is still seen, far more 
                   variation is visible than in the global trend plot.
        ''')
    
    with st.expander("Radioactivity"):
        fig = plt.figure(figsize=(6,6))
        sns.histplot(df_scaled_lowmass,x="radius_val",hue="radioactive")
        plt.xlabel("Charge Radius (z-scaled)",fontsize="x-large")
        plt.ylabel("Count",fontsize="x-large")
        st.pyplot(plt)
        st.caption('''
                   A histrogram of the charge radii where the radioactive distribution (1) is 
                   compared to the stable distribution (0). No clear difference is seen between the 
                   radioactive and stable nuclei. The large count at -1.5 appears to be an outlier.
        ''')
        
    with st.expander("Decay Mode"):
        plt.figure(figsize=(8,4))
        sns.violinplot(df_scaled_lowmass,x=" decay",y="radius_val")
        plt.xlabel("Decay Mode",fontsize="x-large")
        plt.ylabel("Charge Radius (z-scaled)",fontsize="x-large")
        st.pyplot(plt)
        st.caption('''
                   Each decay mode spans various radii distributions. Alpha and double beta-plus 
                   decay are not observed in this region. Beta-minus decays span into the lowest 
                   charge radii seen in the region. Stable, electron capture, and electron capture + beta-plus 
                   all span a similar region.
        ''')
    
    with st.expander("Mass Excess"):
        chart2 = alt.Chart(df_scaled_lowmass).mark_point().encode(
            x=alt.X('MASS EXCESS', title='Mass excess (z-scaled)'),
            y=alt.Y('radius_val', title='Charge Radius (z-scaled)'),
            color=' decay',
            tooltip=['MASS EXCESS', 'radius_val', 'z', 'n', ' decay', ]
            ).interactive()
        st.altair_chart(chart2)
        st.caption('''
                   Charge radii is plotted as a function of the mass excess value.
                   The charge radii roughly follow a linear relationshp with the mass excess values 
                   in this region. Two grouping are observed: a large radii region corresponding to low 
                   mass excess, and a small radii region with a large mass excess.
        ''')
    
    
    with st.expander("Binding Energy per Nucleon"):
        chart3 = alt.Chart(df_scaled_lowmass).mark_point().encode(
            x=alt.X('BINDING ENERGY/A', title="Binding enrgy per nucleon (z-scaled)"),
            y=alt.Y('radius_val', title='Charge radius (z-scaled)'),
            color=' decay',
            tooltip=['BINDING ENERGY/A', 'radius_val', 'z', 'n', ' decay']
            ).interactive()
        st.altair_chart(chart3)
        st.caption('''
                   Charge radii is plotted as a function of the binding energy per nucleon. The colors encode the decay 
                   method of the nucleus. A bimodial distribution is seen in this region with small radii grouped at small 
                   binding energy and a second grouping of larger radii and larger binding energy.
        ''')
    
    st.write('''
             The local evolution of the nuclear charge radius includes many features that are not visible 
             from a global view. The mass number, while still following the general trend of the radii, does not fully explain 
             the distribution seen. In this local view, different trends are observed for the charge radii as compared to the 
             decay mode, mass excess, and binding energy per nucleon. In future work, these relationships will be used to 
             try to predict the charge radius values of nuclei in the shell closure regions.
             ''')