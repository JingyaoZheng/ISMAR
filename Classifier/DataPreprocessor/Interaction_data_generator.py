import re
import os
import pandas as pd
import argparse
from datetime import datetime

def process_notification_data(notification_file, interaction_file, output_excel_file):
    """
    Process notification data and interaction data to create an Excel file
    with an UrgencyLevel column indicating if the index appears in the interaction file.
    
    Args:
        notification_file (str): Path to the notification data file
        interaction_file (str): Path to the interaction data file
        output_excel_file (str): Path to save the output Excel file
    """
    # Read the notification data
    with open(notification_file, 'r', encoding='utf-8') as file:
        notification_lines = file.readlines()
    
    # Read the interaction data
    with open(interaction_file, 'r', encoding='utf-8') as file:
        interaction_lines = file.readlines()
    
    # Extract indexes from interaction data
    interaction_indices = set()
    for line in interaction_lines:
        match = re.search(r'Index: (\d+);', line)
        if match:
            interaction_indices.add(int(match.group(1)))
    
    # Parse notification data
    notifications = []
    for line in notification_lines:
        line = line.strip()
        if not line:
            continue
        
        match = re.match(r'Index: (\d+), Sender: (\w+), Application: (\w+), Content: (.*)', line)
        if match:
            index = int(match.group(1))
            sender = match.group(2)
            application = match.group(3)
            content = match.group(4)
            
            # Check if the index appears in the interaction data
            urgency_level = 1 if index in interaction_indices else 0
            
            notifications.append({
                'Index': index,
                'Sender': sender,
                'Application': application,
                'Content': content,
                'Urgency Level': urgency_level
            })
    
    # Create a DataFrame from the notifications
    df = pd.DataFrame(notifications)
    
    # Save to Excel
    df.to_excel(output_excel_file, index=False)
    print(f"Data successfully saved to {output_excel_file}")
    
    # Print some statistics
    total_notifications = len(df)
    urgent_notifications = df['Urgency Level'].sum()
    
    print(f"Total notifications: {total_notifications}")
    print(f"Notifications with UrgencyLevel=1: {urgent_notifications}")
    print(f"Percentage urgent: {(urgent_notifications/total_notifications)*100:.2f}%")



if __name__ == "__main__":
    
    user_id = input("Enter the user id: ")
    notification_file = f"Data/NotificationData_{user_id}.txt"
    interaction_file = f"Data/User_{user_id}_interaction.txt"
    output_excel_file = f"Data/Interaction_data_{user_id}.xlsx"
    
    process_notification_data(notification_file, interaction_file, output_excel_file)