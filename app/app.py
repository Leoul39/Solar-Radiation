import streamlit as st
import os
import sys 
import matplotlib.pyplot as plt
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from scripts.util import load_data,EDA
lis=['GHI','DHI','DNI','WS','TModA','TModB']
benin,sierraleone,togo=load_data()
eda=EDA(benin,sierraleone,togo)
benin,sierraleone,togo=eda.preprocess()
add_sidebar = st.sidebar.selectbox('Solar Radiation Datasets Analysis',('Summary Statistics',
        'Monthly plot','Daily plot','Correlational heatmap','Histograms','Outlier Detection'))
if add_sidebar == 'Summary Statistics':
    st.title('Summary Statistics')
    st.header("Stats for :blue[Benin] dataframe",divider='blue')
    st.write(benin.describe())
    st.header("Stats for :red[Sierraleone] dataframe",divider='red')
    st.write(sierraleone.describe())
    st.header('Stats for :green[Togo] dataframe',divider='green')
    st.write(togo.describe())
elif add_sidebar == 'Monthly plot':
    st.title(":gray[Monthly Distribution Analysis]")
    st.markdown("The following plot will depict the distribution the column entered for the dataframe mentioned with the rolling means added to it")
    data_name = st.selectbox("Select a dataframe:", ["Benin", "Sierra Leone", "Togo"])
    column_name = st.text_input("Enter the column name from the dataset")
    plot_width = st.slider("Set plot width", 6, 20, 10)  
    plot_height = st.slider("Set plot height", 4, 15, 6)  
    
    if st.button("Plot"):
        if data_name == "Benin":
                selected_data = benin
        elif data_name == "Sierra Leone":
                selected_data = sierraleone
        elif data_name == "Togo":
                selected_data = togo
        else:
                selected_data = None

        if selected_data is not None:
             try:
                
                plt.figure(figsize=(plot_width, plot_height))
                eda.plot_by_month(data=selected_data, column=column_name, name=data_name)
                st.pyplot(plt.gcf())  
             except Exception as e:
                st.error(f"An error occurred: {e}")
elif add_sidebar == 'Daily plot':
      st.title("Daily Distribution of :blue[Irradiance] and :green[Temperature]")
      st.markdown("The following visualizes the hourly distribution of irradiance and temperature")
      data_name = st.selectbox("Select a dataframe:", ["Benin", "Sierra Leone", "Togo"])
      date_name = st.date_input("Pick a date:")
      plot_width = st.slider("Set plot width", 6, 20, 10)
      plot_height = st.slider("Set plot height", 4, 15, 6)  
      if st.button("Plot"):
        if data_name == "Benin":
                selected_data = benin
        elif data_name == "Sierra Leone":
                selected_data = sierraleone
        elif data_name == "Togo":
                selected_data = togo
        else:
                selected_data = None

        if selected_data is not None:
             try:
                
                plt.figure(figsize=(plot_width, plot_height))
                eda.plot_by_day(data=selected_data,date=date_name,name=data_name)
                st.pyplot(plt.gcf())  
             except Exception as e:
                st.error(f"An error occurred: {e}")
elif add_sidebar == 'Correlational heatmap':
        st.title("blue:[Correlational Heatmap]")
        st.markdown("The following is the correlation mapped using seaborn for the 3 datasets")
        fig=eda.correlation()
        st.pyplot(fig)  
elif add_sidebar  == 'Histograms':
      data_name=st.selectbox("Select a dataframe:", ["Benin", "Sierra Leone", "Togo"])
      if st.button("Plot"):
        if data_name == "Benin":
                selected_data = benin
        elif data_name == "Sierra Leone":
                selected_data = sierraleone
        elif data_name == "Togo":
                selected_data = togo
        else:
                selected_data = None

        if selected_data is not None:
             try:
                fig=eda.histogram(data=selected_data,lis=lis,name=data_name)
                st.pyplot(fig)  
             except Exception as e:
                st.error(f"An error occurred: {e}")
elif add_sidebar == 'Outlier Detection':
      data_name=st.selectbox("Select a dataframe:", ["Benin", "Sierra Leone", "Togo"])
      column_name = st.text_input("Enter the column from the dataframe")
      method=st.selectbox('Select a detection method',["iqr","z-score"])
      if st.button("Submit"):
        if data_name == "Benin":
                selected_data = benin
        elif data_name == "Sierra Leone":
                selected_data = sierraleone
        elif data_name == "Togo":
                selected_data = togo
        else:
                selected_data = None

        if selected_data is not None:
             try:
                st.write(eda.detect_outliers(data=selected_data,column=column_name,method=method,name=data_name))
             except Exception as e:
                st.error(f"An error occurred: {e}")