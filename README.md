![Update 6871.github.io](https://github.com/6871/6871.github.io/workflows/Update%206871.github.io/badge.svg)

# What

Publishes graphs showing COVID-19 daily mortality rates by country here:

* [https://6871.github.io/](https://6871.github.io/)

Thanks to [John Hopkins](https://systems.jhu.edu/research/public-health/ncov/)
for sharing their [data](https://github.com/CSSEGISandData/COVID-19); it is
updated daily around 2359 UTC.

# Why

* I couldn't find an existing non-cumulative graph like this
* Death rates may be a better way to compare countries than infection rates:
  * Published infection levels likely correlate with testing ability:
    * Countries with low testing rates may have many unknown infections
    * Countries with high testing rates may have less unknown infections
# How

The following [John Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)
source data file of cumulative deaths is used as a starting point:

* [```time_series_covid19_deaths_global.csv```](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv)

The following script uses the above file to generates a tidy data file
of daily totals (instead of cumulative ones) with optional rolling average
applied:

* [```ci/create_daily_rates_csv.py```](ci/create_daily_rates_csv.py)

A [Plotly](https://plotly.com/) graph HTML ```div``` file is created for each
data file using:

* [```ci/create_graph_div.py```](ci/create_graph_div.py)

The [Plotly](https://plotly.com/) graph ```div``` files are combined into a
simple HTML file with:

* [```ci/create_html_file.sh```](ci/create_html_file.sh)

## GutHub Automated Build

The following [GitHub Action](https://help.github.com/en/actions) automates
updating the main [https://6871.github.io](https://6871.github.io)
[```index.html```](index.html) file so it shows the latest published data:
 
* [```.github/workflows/main.yml```](.github/workflows/main.yml)

## Creating Graphs Locally

```shell script
git clone https://github.com/6871/6871.github.io
cd 6871.github.io
curl -L -O https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv

# Required by scripts
pip3 install setuptools
pip3 install pandas
pip3 install plotly

# Generate 2 daily data sets; one raw, one with 3 day rolling average
python3 ci/create_daily_rates_csv.py time_series_covid19_deaths_global.csv 0
python3 ci/create_daily_rates_csv.py time_series_covid19_deaths_global.csv 3

# Create 2 graphs from the generated data sets
python3 \
  ci/create_graph_div.py daily_mortality_averaged_0_days.csv \
  'COVID-19 Daily Mortality Rate By Country - raw data, no averaging' \
  daily_mortality_averaged_0_days.div

python3 \
  ci/create_graph_div.py daily_mortality_averaged_3_days.csv \
  'COVID-19 Daily Mortality Rate By Country - 3 day running average' \
  daily_mortality_averaged_3_days.div

# Combine the graphs into file tmp.html:
./ci/create_html_file.sh \
  tmp.html \
  daily_mortality_averaged_0_days.div \
  daily_mortality_averaged_3_days.div

# View the graphs:
firefox tmp.html
google-chrome tmp.html
```
