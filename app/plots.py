import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme('notebook')
import pandas as pd
import time
import os 
import sys
import warnings
warnings.filterwarnings("ignore")
#project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.append(project_root)
#from scripts.logger import log

class plots:
    def __init__(self, data1, data2, data3):
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
    def preprocess(self):
        """
        - This method is made for the removal of negative values in the irradiation entries. Since this is 
        probably caused because of an instrumental error, I decided to remove them.

        Parameter:
            None
        Returns:
            Preprocessed datasets where the negative entries are removed.
        """
        #Preprocessing each dataset
        try:
            start=time.time()
            self.data1=(self.data1[(self.data1['GHI']>0)&(self.data1['DHI']>0)&(self.data1['DNI']>0)]).reset_index(drop=True)
            self.data2=(self.data2[(self.data2['GHI']>0)&(self.data2['DHI']>0)&(self.data2['DNI']>0)]).reset_index(drop=True)
            self.data3=(self.data3[(self.data3['GHI']>0)&(self.data3['DHI']>0)&(self.data3['DNI']>0)]).reset_index(drop=True)
            self.data1.drop('Comments',axis=1,inplace=True)
            self.data2.drop('Comments',axis=1,inplace=True)
            self.data3.drop('Comments',axis=1,inplace=True)
            end=time.time()
            return self.data1,self.data2,self.data3
        except Exception as e:
             return None
    def plot_by_month(self, data, column, name,width,height):
        """
        Visualizes a line plot for the specific data and column entered with a rolling mean 
        included and end-of-month markers.
        
        Parameters:
            data: DataFrame to be analyzed
            column: Specific column for visualization
            name: Name of the dataset for titling purposes
        Returns:
            An interactive Plotly line plot
        """
        try:
            start = time.time()

            data['Timestamp'] = pd.to_datetime(data['Timestamp'])
            data = data.set_index('Timestamp')

            # Resample to daily sums for monthly rolling mean
            day = data.resample('D').sum()
            day['rolling'] = day[column].rolling(window=30).mean()

            # Identify end-of-month points
            end_of_month = day[day.index.is_month_end]

            #Generating the plot
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=day.index,
                y=day[column],
                mode='lines',
                name=column,
                line=dict(color='blue', width=2),
                opacity=0.6
            ))
            fig.add_trace(go.Scatter(
                x=day.index,
                y=day['rolling'],
                mode='lines',
                name=f'Rolling Mean ({column})',
                line=dict(color='red', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=end_of_month.index,
                y=end_of_month['rolling'],
                mode='markers',
                name='End of Month',
                marker=dict(color='black', size=8)
            ))
            fig.update_layout(
                title=f'{column} and Monthly Rolling Means with End-of-Month Markers for {name}',
                xaxis_title='Date',
                yaxis_title=column,
                template='plotly_white',
                legend_title='Legend',
                height=height*100,
                width=width*100
            )

            
            end = time.time()
            return fig
        except Exception as e:
            return None


    def plot_by_day(self, data, date, name,width,height):
        """
        Analyzes one specific day and visualizes irradiance (GHI, DNI, DHI) and ambient temperature (Tamb).
        
        Parameters:
            data: DataFrame to be analyzed
            date: Specific date to visualize
            name: Name of the dataset for titling purposes
        Returns:
            Interactive line plots
        """
        try:
            start = time.time()

            # Ensure Timestamp is datetime
            data['Timestamp'] = pd.to_datetime(data['Timestamp'])

            # Filter data for the specific date
            filtered_data = data[data['Timestamp'].dt.date == pd.to_datetime(date).date()]
            
            # Create the figure
            fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=['GHI', 'DHI', 'DNI', 'Tamb'])

            # Add GHI plot
            fig.add_trace(go.Scatter(
                x=filtered_data['Timestamp'],
                y=filtered_data['GHI'],
                mode='lines',
                name='GHI',
                line=dict(color='blue', width=2)
            ), row=1, col=1)

            # Add DHI plot
            fig.add_trace(go.Scatter(
                x=filtered_data['Timestamp'],
                y=filtered_data['DHI'],
                mode='lines',
                name='DHI',
                line=dict(color='red', width=2)
            ), row=2, col=1)

            # Add DNI plot
            fig.add_trace(go.Scatter(
                x=filtered_data['Timestamp'],
                y=filtered_data['DNI'],
                mode='lines',
                name='DNI',
                line=dict(color='green', width=2)
            ), row=3, col=1)

            # Add Tamb plot
            fig.add_trace(go.Scatter(
                x=filtered_data['Timestamp'],
                y=filtered_data['Tamb'],
                mode='lines',
                name='Tamb',
                line=dict(color='orange', width=2)
            ), row=4, col=1)

            # Update layout
            fig.update_layout(
                height=height*100,
                width=width*100,
                title=f'The Solar Irradiance and Ambient Temperature (Tamb) for {name} on date:{date}',
                xaxis_title='Timestamp',
                yaxis_title='Values',
                template='plotly_white',
                showlegend=False
            )
            end = time.time()
            return fig
        except Exception as e:
            return None

    def correlation(self,width,height):
        """
        - This method calculates and plots the correlational heatmap using Plotly. This method uses 
        the initialized parameters for the class and displays them interactively.

        Parameter:
            None (Since the parameters come from the class)
        Returns:
            A dictionary containing the three Plotly heatmaps.
        """
        try:
            start=time.time()
            fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
            sns.heatmap(self.data1[['GHI','DNI','DHI','TModA','TModB']].corr(),annot=True,cmap='coolwarm',ax=axes[0],cbar=False)
            axes[0].set_title('Benin')
            sns.heatmap(self.data2[['GHI','DNI','DHI','TModA','TModB']].corr(),annot=True,cmap='coolwarm',ax=axes[1],cbar=False)
            axes[1].set_title('Sierraleone')
            sns.heatmap(self.data3[['GHI','DNI','DHI','TModA','TModB']].corr(),annot=True,cmap='coolwarm',ax=axes[2])
            axes[2].set_title('Togo')
            fig.suptitle("Correlational Heatmap for some specific columns of each dataset")
            end=time.time()
        except Exception as e:
             return None

    def histogram(self,data,lis,name):
        """
        - This method visualizes the histogram plots for certain mentioned column in the list passes as a 
        parameter.

        Parameter:
            data - data used to analyze
            lis - the list of columns to be used as subplots
            name - name of the dataset
        Returns:
            a subplot of histogram plots
        """
        try:
            start=time.time()
            fig,ax=plt.subplots(nrows=2,ncols=len(lis)//2,figsize=(12,8))
            for i in range(len(lis)//2):
                ax[0,i].hist(data[lis[i]],bins=30)
                ax[0,i].set_title(lis[i])
            for i in range(len(lis)//2):
                ax[1,i].hist(data[lis[i+3]],bins=30)
                ax[1,i].set_title(lis[i+3])
            fig.suptitle(f"The histogram plot of certain columns for {name} dataset")
            end=time.time()
    
        except Exception as e:
            return None
    def detect_outliers(self,data, column, method,name):
        """
        Detects outliers in a given column using IQR or Z-score method.
        
        Parameters:
            data (pd.DataFrame): The dataset.
            column (str): The column name for which to detect outliers.
            method (str): The method to use ("iqr" or "z-score"). Default is "iqr".
            name (str): The name of the dataset
        Returns:
            pd.DataFrame: A sidetable summary of outliers.
        """
        start=time.time()
        
        if method == "iqr":
            # Calculate IQR
            q1 = data[column].quantile(0.25)
            q3 = data[column].quantile(0.75)
            iqr = q3 - q1
            lower_limit = q1 - 1.5 * iqr
            upper_limit = q3 + 1.5 * iqr
            
            # Identify outliers
            outliers = data[(data[column] < lower_limit) | (data[column] > upper_limit)]
        
        elif method == "z-score":
            # Calculate Z-scores
            mean = data[column].mean()
            std = data[column].std()
            data['z_score'] = (data[column] - mean) / std
            
            # Identify outliers
            outliers = data[(data['z_score'].abs() > 3)]
            data = data.drop(columns=['z_score'], errors='ignore')  # Clean up temporary column

        else:
            raise ValueError("Method must be 'iqr' or 'z-score'.")
        
        # Use sidetable for a beautiful summary
        data['outlier'] = data.index.isin(outliers.index)
        summary = data.stb.freq(['outlier'], style=True)
        end=time.time()
        return summary