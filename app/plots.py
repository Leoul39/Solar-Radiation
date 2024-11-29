import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time
import os 
import sys
import warnings
warnings.filterwarnings("ignore")
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from scripts.logger import log

class plots:
    def __init__(self, data1, data2, data3):
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3

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
            log.info(f"Creating Plotly line plot for {column} with monthly rolling means...")
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
            log.info(f"Plotly line plot created in {round(end - start, 2)} seconds.")
            return fig
        except Exception as e:
            log.error(f"Error occurred while creating the plot: {e}")
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
            log.info(f"Creating Plotly plots for irradiance and temperature for {name} on {date}...")
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
            log.info(f"Plotly plots created in {round(end - start, 2)} seconds.")
            return fig
        except Exception as e:
            log.error(f"Error occurred while creating the plots: {e}")
            return None


    def correlations(self,width,height):
        """
        - This method calculates the correlational heatmap using plotly. 
        It uses the initialized parameters for the class and plots them automatically.

        Parameter:
            None (Since the parameters come from the class)
        Returns:
            3 Correlational heatmaps
        """
        try:
            log.info('Loading the correlational heatmap using Plotly...')
            start = time.time()

            from plotly.subplots import make_subplots
            import plotly.graph_objects as go

            # Create subplots for the three datasets
            fig = make_subplots(rows=1, cols=3, subplot_titles=["Benin", "Sierraleone", "Togo"])

            # Benin Heatmap
            corr_benin = self.data1[['GHI', 'DNI', 'DHI', 'TModA', 'TModB']].corr()
            fig.add_trace(
                go.Heatmap(
                    z=corr_benin.values,
                    x=corr_benin.columns,
                    y=corr_benin.columns,
                    colorscale="coolwarm",
                    zmin=-1, zmax=1,
                    colorbar=dict(title="Correlation", len=0.8, y=0.5),
                ),
                row=1, col=1
            )

            # Sierraleone Heatmap
            corr_sierraleone = self.data2[['GHI', 'DNI', 'DHI', 'TModA', 'TModB']].corr()
            fig.add_trace(
                go.Heatmap(
                    z=corr_sierraleone.values,
                    x=corr_sierraleone.columns,
                    y=corr_sierraleone.columns,
                    colorscale="coolwarm",
                    zmin=-1, zmax=1,
                    showscale=False,  
                ),
                row=1, col=2
            )

            # Togo Heatmap
            corr_togo = self.data3[['GHI', 'DNI', 'DHI', 'TModA', 'TModB']].corr()
            fig.add_trace(
                go.Heatmap(
                    z=corr_togo.values,
                    x=corr_togo.columns,
                    y=corr_togo.columns,
                    colorscale="coolwarm",
                    zmin=-1, zmax=1,
                    showscale=False,  
                ),
                row=1, col=3
            )

            # Layout and Title
            fig.update_layout(
                title_text="Correlational Heatmap for Specific Columns of all 3 datasets",
                height=height*100, width=width*100,
                showlegend=False
            )
            end = time.time()
            log.info(f"Loaded the correlational heatmap in {round(end-start,2)} seconds.")
            return fig
        except Exception as e:
            log.error(f"Error occurred as {e}")
            return None
    def histogram(self, data, columns, name,width,height):
        """
        - This method visualizes the histogram plots for certain columns passed in a list.

        Parameters:
            data - Data to be analyzed
            columns - List of columns to create histograms for
            name - Name of the dataset for titling purposes
        Returns:
            Interactive histogram subplots
        """
        try:
            log.info(f"Loading histogram plots using Plotly...")
            start = time.time()

            import plotly.figure_factory as ff

            # Creating a list of histograms
            fig = ff.create_distplot(
                [data[col].dropna() for col in columns], 
                group_labels=columns, 
                show_hist=True, show_rug=False
            )

            fig.update_layout(
                title=f"Histogram for Selected Columns in {name} Dataset",
                xaxis_title="Value",
                yaxis_title="Density",
                legend_title="Columns",
                height=height*100, 
                width=width*100,
            )
            end = time.time()
            log.info(f"Loaded histogram plots in {round(end-start,2)} seconds.")
            return fig
        except Exception as e:
            log.error(f"Error occurred while loading the histograms as {e}")
            return None
