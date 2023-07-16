import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-'

    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': message, 'message_date': dates})

    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M\u202f%p -')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(':\s', message, maxsplit=1)
        if len(entry) >= 2:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages

    # extract additional date/time columns
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    # reordering columns
    df = df[['message_date', 'year', 'month', 'day', 'hour', 'minute', 'user', 'message']]

    return df




