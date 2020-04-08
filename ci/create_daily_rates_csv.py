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


def process(source_csv, rolling_average_days, population_csv):
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

    # Add a Country column to simplify plotly graph line naming
    df['Country'] = \
        df['Country/Region'] + ':' + df['Province/State'].fillna('Main')

    cols = df.columns.tolist()
    print(cols)
    cols = cols[-1:] + cols[:-1]
    print(cols)
    df = df[cols]
    df.to_csv('debug_2.csv')

    # Convert data from compounding to daily deaths
    date_col_1_index = get_first_date_col_index(df.columns)
    for row_ctr in range(len(df.index)):
        # Leave date_col_1_index unchanged (it is daily total)
        for col_ctr in range(len(df.columns) - 1, date_col_1_index, -1):
            df.iloc[row_ctr, col_ctr] = \
                df.iloc[row_ctr, col_ctr] - df.iloc[row_ctr, col_ctr - 1]

    df.to_csv('debug_3.csv')

    # Optional % population conversion; drops rows with no population data
    if population_csv is not None:
        df_pop = pd.read_csv(population_csv)
        df_pop = df_pop.loc[df_pop['Population'] > 0]  # drop if 0 population!
        df = df.loc[df['Country'].isin(df_pop['Key'])]  # drop row if no data
        df.to_csv('debug_4.csv')

        for row_ctr in range(len(df.index)):
            country = df.iloc[row_ctr, 0]
            population = df_pop.loc[
                df_pop['Key'] == country, 'Population'
            ].values[0] * 1000000

            print(f'country={country} population={population}')

            for col_ctr in range(len(df.columns) - 1, date_col_1_index - 1, -1):
                df.iloc[row_ctr, col_ctr] = \
                    df.iloc[row_ctr, col_ctr] / population * 100

    df.to_csv('debug_5.csv')

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

    df.to_csv('debug_6.csv')

    # Order rows by most impacted country (right-most col is latest data)
    df = df.sort_values(by=[df.columns[len(df.columns) - 1]], ascending=False)

    # Use pandas melt to get tidy data set for plotly graphing
    df = pd.melt(
        df,
        # id_vars=['Province/State', 'Country/Region'],
        id_vars=['Country'],
        value_vars=df.columns[get_first_date_col_index(df.columns):],
        var_name='Date',
        value_name='Deaths'
    )

    df.to_csv('debug_7.csv')

    # Convert Date column to datetime to simplify plotly graphing
    df['Date'] = pd.to_datetime(df['Date'])

    # If % population was calculated, append '_pct' to output filename
    out_file = f'daily_mortality_averaged_{rolling_average_days}_days'

    if population_csv is not None:
        out_file += '_pct'

    df.to_csv(out_file + '.csv')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError(
            'usage: source_csv_file rolling_average_days [population_csv]')

    if len(sys.argv) == 3:
        process(sys.argv[1], int(sys.argv[2]), None)
    else:
        process(sys.argv[1], int(sys.argv[2]), sys.argv[3])
