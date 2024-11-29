import unittest
import pandas as pd
import numpy as np

from scripts.util import load_data, EDA

class TestUtil(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Sets up test data and initializes the EDA object.
        """
        # Creating a test dataframe
        cls.data1 = pd.DataFrame({
            'Timestamp': pd.date_range(start='2024-01-01', periods=100, freq='H'),
            'GHI': np.random.uniform(0, 100, size=100),
            'DHI': np.random.uniform(0, 50, size=100),
            'DNI': np.random.uniform(0, 200, size=100),
            'Tamb': np.random.uniform(15, 35, size=100),
            'Comments': [''] * 100
        })
        cls.data2 = cls.data1.copy()
        cls.data3 = cls.data1.copy()

        # Add some negative values to test the preprocessing method
        cls.data1.loc[10:15, ['GHI', 'DHI', 'DNI']] = -1

        # Add a Cleaning column for testing cleaning-related plots
        cls.data1['Cleaning'] = np.random.choice([0, 1], size=100)

        cls.eda = EDA(cls.data1, cls.data2, cls.data3)

    def test_load_data(self):
        """
        Test the load_data function.
        """
        try:
            data1, data2, data3 = load_data()
            self.assertIsInstance(data1, pd.DataFrame)
            self.assertIsInstance(data2, pd.DataFrame)
            self.assertIsInstance(data3, pd.DataFrame)
        except Exception as e:
            self.fail(f"load_data raised an exception: {e}")

    def test_preprocess(self):
        """
        Test the preprocess method for removing negative values and dropping 'Comments' column.
        """
        data1, data2, data3 = self.eda.preprocess()
        # Check no negative values
        self.assertTrue((data1[['GHI', 'DHI', 'DNI']] >= 0).all().all())
        # Check 'Comments' column is dropped
        self.assertNotIn('Comments', data1.columns)

if __name__ == '__main__':
    unittest.main()
    #print(os.getcwd())
