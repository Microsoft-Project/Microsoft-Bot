import os

import pandas as pd

dirname = os.path.dirname(__file__).replace('/DataPipeline', '')


def balance_dataset():
    filename = str(dirname) + '/Dataset/Jan20/Processed/processed_latest.csv'

    total_df = pd.read_csv(filename)

    bug_df = total_df.loc[total_df['labels'] == 'bug']
    enh_df = total_df.loc[total_df['labels'] == 'enhancement']
    que_df = total_df.loc[total_df['labels'] == 'question']

    sizes = [bug_df.shape[0], enh_df.shape[0], que_df.shape[0]]

    min_size = min(sizes)

    removal_list = [bug_df.shape[0] - min_size, enh_df.shape[0] - min_size, que_df.shape[0] - min_size]

    if removal_list[0] > 0:
        bug_df = bug_df.iloc[:bug_df.shape[0] - removal_list[0], :]

    if removal_list[1] > 0:
        enh_df = enh_df.iloc[:enh_df.shape[0] - removal_list[1], :]

    if removal_list[2] > 0:
        que_df = que_df.iloc[:que_df.shape[0] - removal_list[2], :]

    total_df = pd.concat([bug_df, enh_df, que_df])

    filename_balance = str(dirname) + '/Dataset/Jan20/Processed/processed_latest_balanced.csv'

    total_df.to_csv(filename_balance, header=['issue_title', 'body', 'labels', 'category_id', 'body_title'], index=None)


balance_dataset()
