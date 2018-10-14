import pandas as pd
from collections import defaultdict


def merge_dataframes(data, currencies, matching):
    tmp_data = pd.merge(data, currencies, on='currency', how='left')
    data_merged = pd.merge(tmp_data, matching, on='matching_id', how='left')
    data_merged['pln_price'] = data_merged['price'] * data_merged['quantity'] * data_merged['ratio']
    return data_merged


def get_counts_dict(data):
    return data.groupby('matching_id').size().to_dict()


def limit_and_split_data(data):
    data_slices = []
    for _, dataframe in data.groupby('matching_id'):
        top_priced_count = dataframe.iloc[0]['top_priced_count']
        data_slices.append(dataframe.sort_values('pln_price', ascending=False)[:top_priced_count])
    return data_slices


def prepare_output(data):
    data_slices = limit_and_split_data(data)
    counts = get_counts_dict(data)
    res = defaultdict(list)
    for dataframe in data_slices:
        res['matching_id'].append(dataframe.iloc[0]['matching_id'])
        res['total_price'].append(dataframe['pln_price'].sum())
        res['avg_price'].append(dataframe['pln_price'].mean())
        res['currency'].append('PLN')
        res['ignored_products_count'].\
            append(counts[dataframe.iloc[0]['matching_id']] - dataframe.iloc[0]['top_priced_count'])
    return res


def valuation_service():
    currencies = pd.read_csv('csv/currencies.csv')
    data = pd.read_csv('csv/data.csv', index_col='id')
    matching = pd.read_csv('csv/matching.csv', index_col='matching_id')

    merged_data = merge_dataframes(data, currencies, matching)
    res = pd.DataFrame.from_dict(prepare_output(merged_data))

    res.to_csv('csv/top_products.csv', index=False)


if __name__ == '__main__':
    valuation_service()
