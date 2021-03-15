# Final

This project is uses ETL and Machine Learning to monitor for potential stock breakout indicators. Then score those indicators in mongo so that an automated trading bot can query the db to queue up potential candidate to monitor/trade on. The process is detailed in the ppt or keynote file.

The LTSM and Bot itself are not included at this time as they are not complete. However, the ETL is and the machine learning for the news sentiment analysis is complete.

Eventually, I'm hoping to have each aspect of the process as selfcontained python files that reference and update mongo or csvs so that they can be set to cron jobs and run consistently w/o any manual intervention. 
