<!--suppress HtmlDeprecatedAttribute -->
<img align="right" src="https://github.com/6871/6871.github.io/workflows/Graph%20Updater/badge.svg" alt="[Build Status Unavailable]">

# What

Publishes graphs showing COVID-19 daily mortality rates by country here:

* [https://6871.github.io/](https://6871.github.io/)

Thanks to [John Hopkins](https://systems.jhu.edu/research/public-health/ncov/)
for sharing their [data](https://github.com/CSSEGISandData/COVID-19); it is
updated daily around 2359 UTC.

# Why

* I couldn't find existing non-cumulative graphs like these
* Death rates may be less susceptible to under reporting than infection rates

# How

This [John Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)
source data file of cumulative deaths is used as a starting point:

* [```time_series_covid19_deaths_global.csv```](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv)

The file is processed by the following script to generate a tidy data file of
daily totals (instead of cumulative ones); grand totals are added for
countries that only release regional totals, an optional moving average is
applied and totals are optionally converted to deaths as a percentage of a
country's population:

* [```ci/create_daily_rates_csv.py```](ci/create_daily_rates_csv.py)

A [Plotly](https://plotly.com/) graph HTML ```div``` file is created from a
tidy data file using the following script:

* [```ci/create_graph_div.py```](ci/create_graph_div.py)

## GutHub Automated Build

The following [GitHub Action](https://help.github.com/en/actions) automates
updating a set of graph files to reflect the latest published data:
 
* [```.github/workflows/main.yml```](.github/workflows/main.yml)
