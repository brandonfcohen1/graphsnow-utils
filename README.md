# graphsnow-utils

Python script to scrape NOHRSC snow observation text files and create geojson for [SnowGraph](https://www.graphsnow.com). I post the geojson files to s3 and call them from there in the app.

I run this script every day on Heroku Scheduler, and it'll ping me on Slack when complete.
