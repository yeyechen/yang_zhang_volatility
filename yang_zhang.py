import pandas as pd
import os

def yang_zhang(daily_data, time):
    pass

def main():
    pass


if __name__ == '__main__':

    global_path = os.getcwd()

    file_name = 'etf-2020.csv'
    file_path = os.path.join(global_path, file_name)
    etf_data = pd.read_csv(file_name)

    etf_daily_data = etf_data[etf_data['TIME'] == '14:55:00']
    etf_daily_data['time'] = pd.to_datetime(etf_daily_data['DATE'] + ' ' + etf_daily_data['TIME'])
    etf_daily_data = etf_daily_data.set_index('time')
    etf_daily_data = etf_daily_data.rename(columns={'OPEN': 'open'})
    selected_columns = ['open', 'high', 'low', 'close']
    etf_daily_data = etf_daily_data[selected_columns]

    main()