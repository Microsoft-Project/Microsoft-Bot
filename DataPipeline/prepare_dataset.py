import os

import pandas as pd

import DataPipeline.corpus_processor as cp
import DataPipeline.dataset_balancer as balancer

default_array_name = ['bug',
                      'documentation',
                      'duplicate',
                      'enhancement',
                      'good first issue',
                      'help wanted',
                      'invalid',
                      'question',
                      'wontfix']

pd.set_option('display.max_columns', None)

default_array_id = [0, 1, 2, 3, 4, 5, 6, 7, 8]

dirname = os.path.dirname(__file__).replace('/DataPipeline', '')


def process_save(filepath):
    print('____________________')
    print('Saving raw to csv as raw_latest.csv')
    df = pd.read_csv(filepath)
    filepath_raw = os.path.join(dirname, 'Dataset/Jan20/Raw/raw_latest.csv')
    print(filepath_raw)
    df.to_csv(filepath_raw,
              index=None, header=['issue_title', 'body', 'labels', 'category_id'])
    print('Shape of data before processing - ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + 'columns.')

    print('Appending body_title column')
    df['body_title'] = df['body'] + " " + df['issue_title']
    df['body_title'] = df['body_title'].apply(cp.processCorpusSingle)
    print('Shape of data after appending body_title column - ' + str(df.shape[0]) + ' rows and ' + str(
        df.shape[1]) + 'columns.')

    df = df.dropna(subset=['body_title'])
    print('Shape of data after removing null - ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + 'columns.')

    df = df.drop_duplicates(subset=['body_title'], keep='first')
    print(
        'Shape of data after removing duplicates - ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + 'columns.')

    filepath_pro = os.path.join(dirname, 'Dataset/Jan20/Processed/processed_latest.csv')

    print('Saving to csv as processed_latest.csv')
    df.to_csv(filepath_pro, index=None, header=['issue_title', 'body', 'labels', 'body_title', 'category_id'])
    balancer.balance_dataset()
    print('____________________')
