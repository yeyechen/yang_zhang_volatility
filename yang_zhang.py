import pandas as pd
import numpy as np
import os
from math import *

CMT = 20
ALPHA = 1.34
TRADING_DAYS_IN_A_YEAR = 244


def yang_zhang(daily_data):
    """
    Parameters:
        daily_data: data for calculating Yang Zhang volatility at current time, including data for previous CMT days

    Return:
        sigma: Yang Zhang volatility at current time
    """

    # perform row operation to get ln_open/high/low/close_data
    ln_open_data = np.log(daily_data['open'] / daily_data['shifted_close'])
    ln_high_data = np.log(daily_data['high'] / daily_data['open'])
    ln_low_data = np.log(daily_data['low'] / daily_data['open'])
    ln_close_data = np.log(daily_data['close'] / daily_data['open'])

    # calculate Yang Zhang volatility
    ln_open_mean = sum(ln_open_data) / CMT
    ln_close_mean = sum(ln_close_data) / CMT
    V_o = sum((o_i - ln_open_mean) ** 2 for o_i in ln_open_data) * TRADING_DAYS_IN_A_YEAR / (CMT - 1)
    V_c = sum((c_i - ln_close_mean) ** 2 for c_i in ln_close_data) * TRADING_DAYS_IN_A_YEAR / (CMT - 1)
    V_rs = sum(ln_high_data * (ln_high_data - ln_close_data) + ln_low_data * (ln_low_data - ln_close_data)) * TRADING_DAYS_IN_A_YEAR / CMT
    k = (ALPHA - 1) / (ALPHA + (CMT + 1) / (CMT - 1))
    sigma = sqrt(V_o + k * V_c + (1 - k) * V_rs)

    return sigma


def main():
    yz_volatility = []
    trading_time = list(etf_daily_data.iloc[CMT-1:].loc[:, 'time'])

    # set C_0 as O_1, shift down close data
    shifted_close_data_until_time = etf_daily_data['close']
    shifted_close_data_until_time.loc[-1] = etf_daily_data.loc[0, 'open']
    shifted_close_data_until_time.index += 1
    shifted_close_data_until_time.sort_index(inplace=True)
    etf_daily_data['shifted_close'] = shifted_close_data_until_time

    for time in trading_time:
        select_data_until_time = etf_daily_data[etf_daily_data['time'] <= time].tail(CMT).reset_index(drop=True)
        yz_volatility.append(100*yang_zhang(select_data_until_time))

    # output to a csv file
    output = pd.DataFrame({'trading_time': trading_time, 'yang_zhang': yz_volatility})
    save_folder = 'calc_data'
    output_name = 'etf_2020_yang_zhang_daily.csv'
    save_path = os.path.join(global_path, save_folder, output_name)
    output.to_csv(save_path, index=False)


if __name__ == '__main__':
    global_path = os.getcwd()

    file_name = 'etf-2020.csv'
    file_path = os.path.join(global_path, file_name)
    etf_data = pd.read_csv(file_name)

    # select daily 14:55:00 data, combine date and time and set as index, select open/high/low/close as a new DataFrame
    etf_daily_data = etf_data[etf_data['TIME'] == '14:55:00']
    etf_daily_data['time'] = pd.to_datetime(etf_daily_data['DATE'] + ' ' + etf_daily_data['TIME'])
    etf_daily_data = etf_daily_data.rename(columns={'OPEN': 'open'})
    selected_columns = ['time', 'open', 'high', 'low', 'close']
    etf_daily_data = etf_daily_data[selected_columns].reset_index(drop=True)

    main()
