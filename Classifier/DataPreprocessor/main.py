from dataset_combiner import *
from Interaction_data_generator import *

if __name__ == '__main__':

    user_id = input("Enter the user id: ")

    #  Generate the interaction dataset
    notification_file = f"Data/NotificationData_{user_id}.txt"
    interaction_file = f"Data/User_{user_id}_interaction.txt"
    output_excel_file = f"Data/Interaction_data_{user_id}.xlsx"
    process_notification_data(notification_file, interaction_file, output_excel_file)

    #  Generate the final dataset
    self_report_dataset = f'Data/self_report_{user_id}.xlsx'
    combine_datasets(output_excel_file, self_report_dataset)