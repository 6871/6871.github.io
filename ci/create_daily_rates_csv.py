import pandas as pd
import dateutil.parser as dp
import sys
"""
Module to generate CSV file of daily deaths per country for plotly graphs. 
"""


def get_first_date_col_index(header):
    """
    Return the index of the first date formatted column in the header.
    """
    for index, col in enumerate(header):
        try:
            dp.parse(col)
            return index
        except ValueError:
            pass

    raise ValueError(f'No valid date column found in header: {header}')


def get_sub_total_record(df, country):
    """
    Generate a sub total record for the specified country's provinces, but
    exclude the country's (optional) main record; a main record is a row where
    the 'Country/Region' column is set but the 'Province/State' column is not.
    """
    not_null_provinces = df.loc[
        (df['Province/State'].notnull()) &
        (df['Country/Region'] == country)
    ].copy()

    not_null_provinces.loc[:, 'Province/State'] = f'{country} Provinces Sum'

    sub_total_record = not_null_provinces.groupby(
        ['Province/State', 'Country/Region'],
        as_index=False
    ).sum()

    # For now void lat/long (could perhaps use country's capital, for example)
    sub_total_record.loc[0, 'Lat'] = None
    sub_total_record.loc[0, 'Long'] = None

    return sub_total_record


def process(source_csv, rolling_average_days):
    """
    Use source CSV data set to generate a CSV file of daily deaths per country
    that can be used to generate a plotly graph.
    """
    # Load source data set
    df = pd.read_csv(source_csv)

    # Create totals for countries with no main record
    countries_with_total = df.loc[(df['Province/State'].isnull())]
    countries_no_total = \
        df[~df['Country/Region'].isin(countries_with_total['Country/Region'])]

    for country in countries_no_total['Country/Region'].drop_duplicates():
        df = df.append(get_sub_total_record(df, country), ignore_index=True)

    df.to_csv('debug_1.csv')

    # Convert data from compounding to daily deaths
    date_col_1_index = get_first_date_col_index(df.columns)
    for row_ctr in range(len(df.index)):
        # Leave date_col_1_index unchanged (it is daily total)
        for col_ctr in range(len(df.columns) - 1, date_col_1_index, -1):
            df.iloc[row_ctr, col_ctr] = \
                df.iloc[row_ctr, col_ctr] - df.iloc[row_ctr, col_ctr - 1]

    df.to_csv('debug_2.csv')

    # Apply optional rolling average
    if rolling_average_days > 0:
        for row_ctr in range(len(df.index)):
            # Leave date_col_1_index unchanged (it is daily total)
            for col_ctr in range(len(df.columns) - 1, date_col_1_index, -1):
                rolling_sum = 0
                to_col = max(date_col_1_index, col_ctr - rolling_average_days)
                for avg_col_ctr in range(col_ctr, to_col, -1):
                    rolling_sum += df.iloc[row_ctr, avg_col_ctr]

                df.iloc[row_ctr, col_ctr] = rolling_sum / rolling_average_days

    df.to_csv('debug_3.csv')

    # Use pandas melt to get tidy data set for plotly graphing
    df = pd.melt(
        df,
        id_vars=['Province/State', 'Country/Region'],
        value_vars=df.columns[get_first_date_col_index(df.columns):],
        var_name='Date',
        value_name='Deaths'
    )

    df.to_csv('debug_4.csv')

    # Add a Country column to simplify plotly graph line naming
    df['Country'] = \
        df['Country/Region'] + ':' + df['Province/State'].fillna('Main')

    df.to_csv('debug_5.csv')

    # Convert Date column to datetime to simplify plotly graphing
    df['Date'] = pd.to_datetime(df['Date'])
    df.to_csv('debug_6.csv')
    df = df.sort_values(by=['Date', 'Country'])
    df.to_csv(f'daily_mortality_averaged_{rolling_average_days}_days.csv')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError('usage: source_csv_file rolling_average_days')

    process(sys.argv[1], int(sys.argv[2]))
