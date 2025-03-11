import pandas as pd
import numpy as np

def splitData(data_file: str, split_num: int, user_id: str):
    """
    Split the data into two files, one csv and one txt file.

    Args:
        data: str: The path to the data file.
        split_num: int: The number of rows to split the data at.
        user_id: str: The user id to name the files.
    """
    data = pd.read_excel(data_file)
    name_mapping = get_name_mapping(data_file)

    data['Sender'] = data['Sender'].map(name_mapping)

    total_rows = len(data)
    
    # Generate random indices
    random_indices = np.random.choice(total_rows, total_rows, replace=False)
    
    # Split indices
    csv_indices = random_indices[:split_num]
    txt_indices = random_indices[split_num:]

    data_csv = data.iloc[csv_indices]
    data_txt = data.iloc[txt_indices]

    data_csv.to_excel(f'self_report_{user_id}.xlsx', index=False)

    with open(f'NotificationData_{user_id}.txt', 'w', encoding='utf-8') as f:
        for index, row in data_txt.iterrows():
            f.write(
                    f"Index: {row['Index']}, Sender: {row['Sender']}, Application: {row['Application']}, Content: {row['Content']}\n"
                    )
    print("Data split successfully.")


def get_name_mapping(file_path:str):
    """
    Replace generic sender identifiers (Friend1, Boss, OL, etc.) with actual names 
    in an Excel file based on user input from the terminal.
    
    Args:
        file_path: Path to the Excel file
    
    Returns:
        dict: A dictionary mapping the generic sender identifiers to actual names
    """

    df = pd.read_excel(file_path)
    
    unique_senders = df['Sender'].unique()
    
    name_mapping = {'System': 'System', 'Group': 'Group'}

    print("Now we need the names of your best friends, boss, and other important people in your life.")
    for sender in unique_senders:
        if sender not in name_mapping and sender != "System" and sender != "Group":
            name_mapping[sender] = input(f"Please enter the name for sender '{sender}':\n")
    print("Thank you! The names have been saved.\n")

    return name_mapping

def get_integer_input (prompt: str) -> int:
    """
    Get an integer input from the user.

    Args:
        prompt: str: The prompt to display to the user.

    Returns:
        int: The integer input from the user.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


if __name__ == '__main__':
    user_id = get_integer_input("Welcome to our study. Please enter your user id:\n")
    splitData('data.xlsx', 90, user_id)
