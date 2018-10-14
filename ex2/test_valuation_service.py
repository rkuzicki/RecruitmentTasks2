import valuation_service as v
import pandas as pd
import unittest


class TestValuationService(unittest.TestCase):
    def setUp(self):
        data_dict = {'id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                     'price': [1, 2, 3, 2, 1, 2, 3, 2, 1],
                     'currency': ['PLN', 'EUR', 'JPY', 'EUR', 'JPY', 'PLN', 'JPY', 'EUR', 'EUR'],
                     'quantity': [1, 2, 1, 5, 2, 1, 4, 2, 2],
                     'matching_id': [1, 1, 1, 2, 2, 2, 3, 3, 3]}
        currencies_dict = {'currency': ['PLN', 'EUR', 'JPY'],
                           'ratio': [1, 2, 3]}
        matchings_dict = {'matching_id': [1, 2, 3],
                          'top_priced_count': [1, 2, 3]}
        self.data = pd.DataFrame.from_dict(data_dict)
        self.currencies = pd.DataFrame.from_dict(currencies_dict)
        self.matching = pd.DataFrame.from_dict(matchings_dict)

    def test_get_counts_dict(self):
        response = v.get_counts_dict(self.data)
        expected_response = {1: 3, 2: 3, 3: 3}
        self.assertEqual(response, expected_response)

    def test_merged_dataframe(self):
        expected_prices = [1, 8, 9, 20, 6, 2, 36, 8, 4]
        expected_top_priced_counts = [1, 1, 1, 2, 2, 2, 3, 3, 3]
        merged_dataframe = v.merge_dataframes(self.data, self.currencies, self.matching)
        self.assertEqual(list(merged_dataframe['pln_price'].values), expected_prices)
        self.assertEqual(list(merged_dataframe['top_priced_count'].values), expected_top_priced_counts)

    def test_output_dict(self):
        expected_output = {'matching_id': [1, 2, 3],
                           'total_price': [9, 26, 48],
                           'avg_price': [9.0, 13.0, 16.0],
                           'currency': ['PLN', 'PLN', 'PLN'],
                           'ignored_products_count': [2, 1, 0]}
        merged_data = v.merge_dataframes(self.data, self.currencies, self.matching)
        output = v.prepare_output(merged_data)
        self.assertEqual(expected_output, output)




