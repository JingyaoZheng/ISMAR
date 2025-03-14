import pandas as pd
import re
import argparse

def combine_datasets(interaction_dataset, self_report_dataset):
    """
    Combine two datasets into a single dataset and write it into one excel file.
    It also adds a column 'Datasource' to indicate the source of the data.
    1 refers to the interaction data, and 0 refers to the self-report data.
    
    Args:
        interaction_dataset (str): Path to the interaction dataset file.
        self_report_dataset (str): Path to the self-report dataset file.

    """
    interaction_data = pd.read_excel(interaction_dataset)
    interaction_data['Datasource'] = 1 
    self_report_data = pd.read_excel(self_report_dataset)
    self_report_data['Datasource'] = 0

    user_id = re.search(r'(\d+)', interaction_dataset).group(1)
    combined_data = pd.concat([interaction_data, self_report_data], ignore_index=True)
    combined_data = combined_data.sort_values(by='Index')
    combined_data.to_excel(f'Data/combined_dataset_{user_id}.xlsx', index=False)

if __name__ == '__main__':

    interaction_dataset = 'Data/Interaction_data_1.xlsx'
    self_report_dataset = 'Data/self_report_1.xlsx'

    combine_datasets(interaction_dataset, self_report_dataset)