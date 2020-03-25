import numpy as np 
import datetime 
import pandas as pd


class TransactionFeatures():
    """
    A class to do the feature engineering of the transactional data. The end goal is to have a data frame 
    where on user_id has one row of features. This data frame can then be used in many ML models
    """
    def __init__(
        self,
        data: pd.DataFrame,
        last_n_txn=3,
        first_n_txn=3
        ):
        # A data set that has the columns user_id, created_date, amount_usd, direction, transactions_type
        # Note that the created_date column needs to be a datetime object
        self.data = data

        # A constant defining how many of the first transactions per user to 
        # take into account when deriving variables associates with the 
        # first transactions
        self.last_n_txn = last_n_txn

        # A constant defining how many of the last transactions per user to 
        # take into account when deriving variables associates with the 
        # first transactions
        self.first_n_txn = first_n_txn

    def get_transaction_date(self):
        """
        A method to get the transaction date (YYYY-MM-DD). The column is created to the 
        data object with which the class was created
        """
        self.data['transaction_day'] = [x.date() for x in self.data['created_date']]

    def get_avg_sent(self) -> pd.DataFrame:
        """
        A method that aggregates the sent amount per user
        """
        return self.data.groupby('user_id', as_index=False)['amount_usd'].mean()

    def get_avg_txn(self) -> pd.DataFrame:
        """
        A method to calculate the average amount of transactions sent per day
        """    
        return self.data.groupby('user_id', as_index=False).apply(lambda x: pd.DataFrame({
            'user_id': [x['user_id'].tolist()[0]],
            'avg_txn': [x.shape[0]/len(set(x['transaction_day']))]
        }))

    def get_distribution_transaction_type(self, feature: str) -> pd.DataFrame:
        """
        A method to calculate the distribution of transactions by the given feature
        """    
        grouped = self.data.groupby(['user_id', feature], as_index=False)['transaction_id'].count()
        grouped = grouped.rename(columns={'transaction_id': 'txn'})
        grouped = grouped.pivot_table(index='user_id', columns=feature, values='txn').fillna(0)

        # Calculating the shares 
        grouped = grouped.apply(lambda x: x/np.sum(x), axis=1)

        # Returning 
        return grouped

    @staticmethod
    def get_first_last_txn_stats(
        data: pd.DataFrame, 
        first_n_txn: int, 
        last_n_txn: int,
        sort_by_time_var=True,
        time_var='created_date') -> pd.DataFrame:
        """
        A method to get the behaviour of the first n transactions and the last n transactions. 
        The data needs to be sorted by the time variable
        """ 
        if sort_by_time_var:    
            data = data.sort_values([time_var])

        # Subseting the first_n transactions
        first = data.head(first_n_txn)
        
        # Subsetting the last_n transactions
        last = data.tail(last_n_txn)

        # Calculating the statistics 
        mean_first = np.mean(first['amount_usd'])
        mean_last = np.mean(last['amount_usd'])

        diff_days_first = np.nanmean([x.days for x in first['created_date'].diff()])
        diff_days_last = np.nanmean([x.days for x in last['created_date'].diff()])

        diff_means = mean_last - mean_first
        diff_days = diff_days_last - diff_days_first

        # Returning the data frame 
        return pd.DataFrame({
            'diff_mean_amount_sent': [diff_means],
            'diff_days_between_txn': [diff_days]
            })

    def return_last_first_stats(self) -> pd.DataFrame:
        """
        A method to use the function get_first_last_txn_stats
        """
        return self.data.groupby(['user_id']).apply(lambda x: self.get_first_last_txn_stats(
            data=x, 
            first_n_txn=self.first_n_txn,
            last_n_txn=self.last_n_txn
            )).droplevel(1)        

    def feature_engineering_pipeline(self) -> pd.DataFrame:
        """
        A method that wraps every feature engineering step and outputs 
        a preprocesed data frame 
        """ 
        # Getting the date        
        self.get_transaction_date()

        # Calculating the average amount sent 
        d = self.get_avg_sent()

        # Calculating the mean daily transaction count 
        d = pd.merge(d, self.get_avg_txn(), on='user_id')

        # Getting the distribution of txn per transaction type 
        d = pd.merge(
            d, 
            self.get_distribution_transaction_type('transactions_type'), 
            left_on='user_id', 
            right_index=True
            )

        # Getting the distribution of txn per direction
        d = pd.merge(
            d, 
            self.get_distribution_transaction_type('direction'),
            left_on='user_id', 
            right_index=True
            ) 

        # Returnign the data frame 
        return d