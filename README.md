# CMSE830_MIDTERM
Midterm project for CMSE 830

In this project, I am exploring the connection between the nuclear charge radius and other properties of the nucleus. Measurements of nuclear charge radii are the focus of my PhD thesis project. The nuclear charge radius provides information about the proton distribution in the nucleus. Throughout the nuclear chart, the charge radius can be modeled by a simple power law forumula, but in local ranges (especially around rare phenomena like nuclear shell closures) the charge radii exhibits intersting behavior. Therefore, I show the relationship between key features and the charge radius in both an overall and local example.

I gathered data from international atomic energy agency, which maintains several tabels of nuclear data. I used the charge radius (1), mass (2), and lifetime (3) tables which are linked below and included in the github.
1. https://www-nds.iaea.org/radii/; charge_radii.xlsx
2. https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt; nuclear_mass.xlsx
3. https://www-nds.iaea.org/relnsd/NdsEnsdf/QueryForm.html; lifetime.csv

I combined these tables into a single cleaned data set with data_cleaning.ipynb program, and that data is saved as combined_data.csv. I generated visualizations from the eda_visualizaiton.ipynb, and encoprporated many of these visualizations in the streamlit app. The streamlit app is run from the streamlit_app.py file. In order to run the notebooks, the following packages are needed:
1. numpy
2. pandas
3. matplotlib
4. scikit-learn
5. seaborn
6. altair

In the final project, I aim to try to predict the charge radius from the features shown in this midterm project. I hope to improve upon the power law model for the global distribution, and train models on the region around shell closures. 
