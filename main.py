import pandas as pd
from ETL_Functions.functions import get_timestamp, clean_timestamp, get_json_data, clean_extract_two_hour, \
    clean_extract_one_day, clean_extract_four_day, plot_four_day
from loguru import logger
from constants import half_urls


def ETL_Functions():
    """
    Long ETL function where all extract, transform and load functions are called.
    """
    try:
        logger.info('Entering main ETL function')
        #Clean, get and transform local time to required format
        current_timestamp = get_timestamp()
        cleaned_timestamp = clean_timestamp(current_timestamp)

        logger.info("Scraping data from government weather api")
        #Get data for different time intervals in json format from gov api
        two_hour_data = get_json_data(cleaned_timestamp, half_urls[0])
        one_day_data = get_json_data(cleaned_timestamp, half_urls[1])
        four_day_data = get_json_data(cleaned_timestamp, half_urls[2])

        logger.info("Extracting and cleaning data")
        #Extract and clean data, and store them in pandas dataframes
        two_hour_df = clean_extract_two_hour(two_hour_data)
        one_day_df = clean_extract_one_day(one_day_data)
        four_day_df = clean_extract_four_day(four_day_data)

        logger.info("Writing complete data to csv")
        #Writing multiple dataframes with titles to single csv file
        empty_data = ['']
        two_hour_header = pd.DataFrame(empty_data, columns=["2 Hour Forecast"])
        twenty_four_hour_header = pd.DataFrame(empty_data, columns=["24 Hour Forecast"])
        four_day_header = pd.DataFrame(empty_data, columns=["4 Day Forecast"])
        empty_row = pd.DataFrame(empty_data, columns=[""])
        with open('Weather_Data.csv', mode='a+'):
            two_hour_header.to_csv('Weather_Data.csv', mode='a', index=False)
            two_hour_df.to_csv('Weather_Data.csv', mode='a', index=False)
            empty_row.to_csv('Weather_Data.csv', mode='a', index=False, header=False)
            twenty_four_hour_header.to_csv('Weather_Data.csv', mode='a', index=False)
            one_day_df.to_csv('Weather_Data.csv', mode='a', index=False)
            empty_row.to_csv('Weather_Data.csv', mode='a', index=False, header=False)
            four_day_header.to_csv('Weather_Data.csv', mode='a', index=False)
            four_day_df.to_csv('Weather_Data.csv', mode='a', index=False)

        logger.info('Generating temperature and humidity graph')
        #Plot four day temp/humidity graph
        four_day_graph = plot_four_day(four_day_df)
        logger.info('Program successfully ran and generated appropriate files, and will exit now')
        return 'OK'
    except Exception as e:
        logger.exception(e)
        return str(e)


full_run = ETL_Functions()