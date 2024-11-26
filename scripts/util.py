import pandas as pd
import os
import time
from scripts.logger import log
import matplotlib.pyplot as plt
import seaborn as sns
import sidetable
def load_data():
        """
        - This method intends to load the datasets.
        
        Parameter:
            None
        Returns:
            The 3 solar radiation datasets loaded from local machine.
        """
        #Loading each dataset using pandas
        try:
            start=time.time()
            log.info("Loading the datasets ...")
            data1 = pd.read_csv('data/benin-malanville.csv')
            data2 = pd.read_csv('data/sierraleone-bumbuna.csv')
            data3 = pd.read_csv('data/togo-dapaong_qc.csv')
            end=time.time()
            log.info(f"Loaded all three datasets after {round(end-start,2)} seconds")
            return data1,data2,data3
        except Exception as e:
            log.error(f"Error occured as {e}")
            return None
class EDA:
    def __init__(self,data1,data2,data3):
        self.data1=data1
        self.data2=data2
        self.data3=data3
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
            log.info("Removing all negative entries for irradiance...")
            start=time.time()
            self.data1=(self.data1[(self.data1['GHI']>0)&(self.data1['DHI']>0)&(self.data1['DNI']>0)]).reset_index(drop=True)
            self.data2=(self.data2[(self.data2['GHI']>0)&(self.data2['DHI']>0)&(self.data2['DNI']>0)]).reset_index(drop=True)
            self.data3=(self.data3[(self.data3['GHI']>0)&(self.data3['DHI']>0)&(self.data3['DNI']>0)]).reset_index(drop=True)
            self.data1.drop('Comments',axis=1,inplace=True)
            self.data2.drop('Comments',axis=1,inplace=True)
            self.data3.drop('Comments',axis=1,inplace=True)
            end=time.time()
            log.info(f"Removed all negative values for irradiance and dropped the 'Comments' column in {round(end-start,2)} seconds")
            return self.data1,self.data2,self.data3
        except Exception as e:
             log.error(f"Error occured as {e}")
             return None
    def plot_by_month(self,data,column,name):
        """
        - This method visualizes the line plot for the specific data and column entered with a rolling means 
        included and the End-of-Month marked specifically.
        Parameter:
            data - data you want to analyze
            column - specific column from the data
            name - name of the data for title and naming purposes
        Returns:
            A line plot
        """
        try:
                start=time.time()
                log.info(f"Loading the line plot for {column} column with the monthly rolling means included...")
                # Ensure Timestamp is datetime and set it as the index
                data['Timestamp'] = pd.to_datetime(data['Timestamp'])
                dataa=data.set_index('Timestamp')

                # Resample to daily sums (already done as benin_day in your code) for monthly rolling
                day = dataa.resample('D').sum()

                # Calculate rolling mean (monthly)
                day['rolling'] = day[column].rolling(window=30).mean()

                # Identify end-of-month points
                end_of_month = day[day.index.is_month_end]

                # Plot the data
                plt.figure(figsize=(12, 6))

                # Plot GHI
                plt.plot(day.index, day[column], label=column, color='blue', alpha=0.6)

                # Plot smoothed GHI
                plt.plot(day.index, day['rolling'], label=f'Rolling means for {column} per month', color='red', linewidth=2)

                # Mark end-of-month points on the smoothed line
                plt.scatter(end_of_month.index, end_of_month['rolling'], color='black', label='End of Month', zorder=5)

                # Customize the plot
                plt.title(f'{column} and Monthly rolling means with End-of-Month Markers for {name} dataset', fontsize=14)
                plt.xlabel('Date', fontsize=12)
                plt.ylabel(column, fontsize=12)
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
                end=time.time()
                log.info(f"Loaded the line plot in {round(end-start,2)} seconds.")
        except Exception as e:
             log.error(f"Error occured while loading plot as {e}")
             return None
             
    def plot_by_day(self,data,date,name):
        """
        - This method specifically analyzes one day entered in the date parameter. Columns analyzed are irradiance
        columns (GHI, DNI, DHI) and Ambient Temperature(Tamb).
        Parameter:
            data- data to be analyzed
            date - the specific date 
            name - name of the dataset for titling purposes.
        Returns:
            A line subplots with the 4 columns depicted
        """
        try:
            log.info(f"Loading the 4 plots considering irradince and temp for {name} dataset on date:{date}...")
            start=time.time()
            data['Timestamp']=pd.to_datetime(data['Timestamp'])
            # Loading the specific date mentioned
            filtered_data = data[data['Timestamp'].dt.date == pd.to_datetime(date).date()]
            # Loading the plots
            fig,ax=plt.subplots(nrows=4,ncols=1,figsize=(12,12))
            filtered_data.plot(x='Timestamp',y='GHI',ax=ax[0],color='blue')
            # For GHI
            ax[0].set_title('Global Horizontal Irradiance (GHI)', fontsize=12)
            ax[0].set_ylabel('GHI', fontsize=10)
            # For DHI
            filtered_data.plot(x='Timestamp',y='DHI',ax=ax[1],color='red')
            ax[1].set_title('Diffuse Horizontal Irradiance (DHI)', fontsize=12)
            ax[1].set_ylabel('DHI', fontsize=10)
            # For DNI
            filtered_data.plot(x='Timestamp',y='DNI',ax=ax[2],color='green')
            ax[2].set_title('Direct Normal Irradiance (DNI)', fontsize=12)
            ax[2].set_ylabel('DNI', fontsize=10)
            # For Tamb
            filtered_data.plot(x='Timestamp',y='Tamb',ax=ax[3],color='orange')
            ax[3].set_title('Ambient Temperature (Tamb)', fontsize=12)
            ax[3].set_ylabel('Tamb', fontsize=10)
            # Arranging the layout
            plt.tight_layout(pad=1.0)
            fig.suptitle(f"Different Solar irradiance and ambient temp. values for {name} dataset on date:{date}", fontsize=16, y=1.02)
            end=time.time()
            log.info(f"Loaded all 4 subplots for the specific date in {round(end-start,2)} seconds.")
        except Exception as e:
             log.error(f"Error while loading the subplots as {e}")
             return None
        
    def plot_cleaning(self,data,column,name):
        """
        - This method portrays the effect of cleaning of the specified column.
        Parameter:
            data - data to be analyzed
            column - the specific column to be analyzed
            name -  name of the dataset for titling purposes.
        Returns:
            A line plot 
        """
        log.info('Loading the plots for the cleaning session...')
        start=time.time()
        before_cleaning = data[data['Cleaning'] == 0]
        after_cleaning = data[data['Cleaning'] == 1]
        plt.figure(figsize=(15,8))
        # Calculate mean readings over time for ModA
        moda_mean_before = before_cleaning.groupby('Timestamp')[column].mean()
        moda_mean_after = after_cleaning.groupby('Timestamp')[column].mean()
        # Plot before cleaning
        plt.plot(moda_mean_before.index, moda_mean_before, label='Before Cleaning', color='orange', alpha=0.7)

        # Plot after cleaning
        plt.plot(moda_mean_after.index, moda_mean_after, label='After Cleaning', color='black', alpha=0.7)
        plt.title(f'Impact of Cleaning on {column} Sensor Readings for {name} dataset', fontsize=14)
        plt.xlabel('Timestamp', fontsize=12)
        plt.ylabel(f'{column} Sensor Reading', fontsize=12)
        plt.legend()
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()
        end=time.time()
        log.info(f"Loaded the cleaning plot in {round(end-start,2)} seconds.")

    def correlation(self):
        """
        - This method calculates the correlational heatmap using seaborn. This method uses the initalized 
        paramters for the class and plots them automatically.

        Parameter:
            None (Since the parameters come from the class)
        Returns:
            3 Correlational heatmaps
        """
        try:
            log.info('Loading the correlational heatmap...')
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
            log.info(f"Loaded the correlational heatmap for all datasets in {round(end-start),2} seconds.")
        except Exception as e:
             log.error(f"Error occured as {e}")
             return None

    def humidity(self,data):
        """
        This method calculates the relationship between the Relative Humidity (RH) and the Temperature and 
        irradiance
        Parameter:
            data - data to be analyzed
        Returns:
            Subplots
        """
        try:
             
            start=time.time()
            log.info("Calculating the relative humidity plots...")
            benin_day = data.resample('D').mean()
            fig,ax=plt.subplots(nrows=1,ncols=2,figsize=(15,8),sharex=True)
            benin_day.plot(kind='scatter',x='RH',y='TModA',ax=ax[0])
            ax[0].set_title(f"Plot for TModA")
            ax[0].set_ylabel('TModA')
            benin_day.plot(kind='scatter',x='RH',y='GHI',ax=ax[1])
            ax[1].set_title(f"Plot for TModB")
            ax[1].set_ylabel('TModB')
            plt.legend()
            plt.xticks(rotation=45)
            end=time.time()
            log.info(f'Loaded the plots in {round(end-start,2)} seconds.')
        except Exception as e:
             log.error(f"Error occured while plotting as {e}")
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
            log.info(f"Loading histogram plots...")
            fig,ax=plt.subplots(nrows=2,ncols=len(lis)//2,figsize=(12,8))
            for i in range(len(lis)//2):
                ax[0,i].hist(data[lis[i]],bins=30)
                ax[0,i].set_title(lis[i])
            for i in range(len(lis)//2):
                ax[1,i].hist(data[lis[i+3]],bins=30)
                ax[1,i].set_title(lis[i+3])
            fig.suptitle(f"The histogram plot of certain columns for {name} dataset")
            end=time.time()
            log.info(f'Loaded each histogram subplots in {round(end-start,2)} seconds.')
        except Exception as e:
            log.error(f"Error occured while loading the histograms as {e}")
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
        log.info(f"Preparing the dataframe for the outliers and non-outliers for {name} dataset using {method} method")
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
        log.info(f"Finished loading the dataframe in {round(end-start,2)} seconds.")
        return summary
        



            
