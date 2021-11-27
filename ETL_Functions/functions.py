import pytz
import datetime as dt
from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt


def get_timestamp():
    """
    Return timestamp in datetime format to be attached to end of website url.
    """
    singapore = pytz.timezone('Asia/Kuala_Lumpur')
    general_time_now = dt.datetime.now()
    localized_time_now = singapore.localize(general_time_now)
    return localized_time_now


def clean_timestamp(timestamp):
    """
    Format timestamp for url.
    """
    datetime_string_slice = str(timestamp)[:19]
    edited_string = datetime_string_slice.replace(':', '%3A').replace(' ', 'T')
    return edited_string


def get_json_data(date_string, half_url):
    """
    Grabs json data from gov api website.
    """
    full_url = half_url + date_string
    response = urlopen(full_url)
    data_json = json.loads(response.read())
    return data_json


def clean_extract_two_hour(json_data):
    """
    Extracts forecast data for all areas in Singapore for a 2 hour time period, and puts data in a pandas dataframe.
    """
    all_data = json_data['items']
    forecast_data = all_data[0]['forecasts']
    area_info = [i['area'] for i in forecast_data]
    forecast_info = [i['forecast'] for i in forecast_data]
    complete_dataframe = pd.DataFrame(list(zip(area_info, forecast_info)), columns=['Area', 'Forecast'])
    return complete_dataframe


def clean_extract_one_day(json_data):
    """
    Extracts forecast data for all areas in Singapore for a 1 day/24 hour time period, and puts data in a pandas dataframe.
    """
    #Data preparation/consolidation
    all_data = json_data['items']
    forecast_data = all_data[0]['periods']
    areas = ['west', 'east', 'central', 'south', 'north']
    times = [i['time']['start'][:19].replace('T', ' ') for i in forecast_data]
    consolidated_data = []
    for i in range(len(times)):
        data_by_time = [forecast_data[i]['regions'][n] for n in areas]
        data_by_time.insert(0, times[i])
        consolidated_data.append(data_by_time)

    #Create and append to dataframe
    column_names = ["Timings", "West", "East", "Central", "South", "North"]
    df = pd.DataFrame(columns=column_names)
    for i in consolidated_data:
        a_series = pd.Series(i, index=df.columns)
        df = df.append(a_series, ignore_index=True)
    return df


def clean_extract_four_day(json_data):
    """
    Extracts forecast data for all areas in Singapore for a 4 day time period, and puts data in a pandas dataframe.
    """
    all_data = json_data['items']
    forecast_data = all_data[0]['forecasts']
    dates = [i['date'] for i in forecast_data]
    forecasts = [i['forecast'] for i in forecast_data]
    average_temps = [(i['temperature']['low'] + i['temperature']['high']) / 2 for i in forecast_data]
    average_humidity = [(i['relative_humidity']['low'] + i['relative_humidity']['high']) / 2 for i in forecast_data]
    complete_dataframe = pd.DataFrame(list(zip(dates, forecasts, average_temps, average_humidity)),
                                      columns=['Date', 'Forecast', 'Average Temperature', 'Average Humidity'])
    #Change float to string to remove trailing zeroes for neatness
    complete_dataframe['Average Temperature'] = complete_dataframe['Average Temperature'].astype(str)[0:4]
    complete_dataframe['Average Humidity'] = complete_dataframe['Average Humidity'].astype(str)[0:4]
    return complete_dataframe


def plot_four_day(df):
    """
    Plot temp and humidity on graph and export to png.
    """
    #Convert string values to float to accurate plot numerical values
    df['Average Temperature'] = df['Average Temperature'].astype(float)
    df['Average Humidity'] = df['Average Humidity'].astype(float)

    plt.plot('Date', 'Average Temperature', data=df, marker='o', color='blue')
    plt.plot('Date', 'Average Humidity', data=df, marker='o', color='red')
    plt.title('Average temperature and humidity for next 4 days')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Humidity/Temp in degrees', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.savefig('Four_day_temp_humidity_graph.png', bbox_inches='tight')













