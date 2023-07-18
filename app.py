import pandas as pd
import re
from datetime import datetime as dt


# Function to extract the day from the date
def get_day(date):
    datetime_obj = dt.strptime(date, '%m/%d/%y')
    return datetime_obj.strftime('%A')

# Read the WhatsApp chat text file
with open('whatsapp_chat.txt', 'r', encoding='utf-8') as file:
    chat_lines = file.readlines()

# Parse the chat lines and extract the relevant information
data = []
chat_datetime = ''
username = ''
message = ''
media_file = ''

for line in chat_lines:
    line = line.strip()
    if line:
        if line.startswith(tuple('0123456789')):
            if username and (message or media_file):
                data.append([date, day, time, username.strip(), message.strip(), media_file.strip()])
            chat_datetime, sender_message = line.split(' - ', 1)
            date, time = chat_datetime.split(', ')
            day = get_day(date)
            if ':' in sender_message:
                username, message = sender_message.split(':', 1)
                media_file = ''
            else:
                username = ''
                message = ''
                media_file = ''
        elif 'IMG' in line and '(file attached)' in line:
            matches = re.findall(r'IMG[^:]*', line)
            if matches:
                media_file = matches[0]
        else:
            if media_file:
                media_file += ' ' + line

# Append the last extracted message
if username and (message or media_file):
    data.append([date, day, time, username.strip(), message.strip(), media_file.strip()])

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=['Date', 'Day', 'Time', 'Username', 'Message', 'Media File'])

# Export the DataFrame to an Excel file
df.to_excel('whatsapp_chat.xlsx', index=False)
