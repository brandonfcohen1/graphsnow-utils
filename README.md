# graphsnow-utils

Python script to scrape NOHRSC snow observation text files and create geojson for [SnowGraph](https://www.graphsnow.com). I post the geojson files to s3 and call them from there in the app.

I run this script every 6 hours on Heroku Scheduler. There is a dummy flask App set up just for deployment to Heroku. There are better ways to do this but this was a quick start.
