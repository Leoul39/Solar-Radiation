#Loading important libraries
import streamlit as st
import pandas as pd

# Loading the necessary scripts from plots and util
from plots import plots

# Columns for the histogram plot
lis=['GHI','DHI','DNI','WS','TModA','TModB']

#Loading the datasets manually
benin=pd.read_csv('data/benin-malanville.csv')
sierraleone=pd.read_csv('data/sierraleone-bumbuna.csv')
togo=pd.read_csv('data/togo-dapaong_qc.csv')
# Initializing the class
plots=plots(benin,sierraleone,togo)

# Preprocess to remove negative entries
benin,sierraleone,togo=plots.preprocess()

# Setting the page and the streamlit app
st.set_page_config(page_title="Solar Radiation Analysis", page_icon="🌞", layout="wide", initial_sidebar_state="expanded")
add_sidebar = st.sidebar.selectbox('Solar Radiation Datasets Analysis',('📊 Summary Statistics',
       '📅 Monthly plot','📆 Daily plot','🗺️ Correlational heatmap','📈 Histograms','🚨 Outlier Detection'))

if add_sidebar == '📊 Summary Statistics':
    st.title('📊 Summary Statistics')
    st.header("Stats for :blue[Benin] dataframe",divider='blue')
    st.write(benin.describe())
    st.header("Stats for :red[Sierraleone] dataframe",divider='red')
    st.write(sierraleone.describe())
    st.header('Stats for :green[Togo] dataframe',divider='green')
    st.write(togo.describe())
elif add_sidebar == '📅 Monthly plot':
    st.title("📅 :blue[Monthly Plot]")
    st.markdown("The following plot will depict the distribution the column entered for the dataframe mentioned with the rolling means added to it")
    data_name = st.selectbox("Select a dataframe:", ["Benin", "Sierra Leone", "Togo"])
    column_name = st.text_input("Enter the column name from the dataset")
    plot_width = st.slider("Set plot width", 6, 30, 20)  
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
                fig=plots.plot_by_month(data=selected_data, column=column_name, name=data_name,width=plot_width,height=plot_height)
                if fig:
                        st.plotly_chart(fig,use_container_width=True)  
             except Exception as e:
                st.error(f"An error occurred: {e}")
elif add_sidebar == '📆 Daily plot':
      st.title("📆 :blue[Daily Plot]")
      st.markdown("The following visualizes the hourly distribution of irradiance and temperature")
      data_name = st.selectbox("Select a dataframe:", ["Benin", "Sierra Leone", "Togo"])
      date_name = st.date_input("Pick a date (from 2021-10-30 to 2022-10-30):")
      plot_width = st.slider("Set plot width", 6, 30, 20)
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
                fig= plots.plot_by_day(data=selected_data,date=date_name,name=data_name,width=plot_width,height=plot_height)
                if fig:
                        st.plotly_chart(fig,use_container_width=True)  
             except Exception as e:
                st.error(f"An error occurred: {e}")
elif add_sidebar == '🗺️ Correlational heatmap':
        st.title("🗺️ :blue[Correlation Heatmap]")
        st.markdown('''
                The following is a correlational heatmap for:

                1. **GHI** (Global Horizontal Irradiance)  
                2. **DHI** (Diffuse Horizontal Irradiance)  
                3. **DNI** (Diffuse Normal Irradiance)  
                4. **WS** (Wind Speed)  
                5. **TModA** (Temperature measured from Mod A)  
                6. **TModB** (Temperature measured from Mod B)
                ''')
        plot_width = st.slider("Set plot width", 6, 30, 20)
        plot_height = st.slider("Set plot height", 4, 15, 6)  
        if st.button('Generate'):
                fig=plots.correlation(width=plot_width,height=plot_height)
                st.pyplot(fig)
elif add_sidebar  == '📈 Histograms':
        st.title("📈 :blue[Histograms]")
        st.markdown('''
                The following is a correlational heatmap for:

                1. **GHI** (Global Horizontal Irradiance)  
                2. **DHI** (Diffuse Horizontal Irradiance)  
                3. **DNI** (Diffuse Normal Irradiance)  
                4. **WS** (Wind Speed)  
                5. **TModA** (Temperature measured from Mod A)  
                6. **TModB** (Temperature measured from Mod B)
                ''')
        data_name=st.selectbox("Select a dataframe:", ["Benin", "Sierra Leone", "Togo"])
        plot_width = st.slider("Set plot width", 6, 30, 20)
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
                                fig=plots.histogram(data=selected_data,lis=lis,name=data_name)
                                st.pyplot(fig)  
                        except Exception as e:
                                st.error(f"An error occurred: {e}")
elif add_sidebar == '🚨 Outlier Detection':
      st.title("🚨 :blue[Outlier Detection]")
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
                st.write(plots.detect_outliers(data=selected_data,column=column_name,method=method,name=data_name))
             except Exception as e:
                st.error(f"An error occurred: {e}")