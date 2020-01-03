### Getting Started

#### Prerequisite

1. [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

2. Python package: pymongo (others please based on error infomation, I forget...

#### Installing

1. First, start MongoDB service (modify the instruction based on your own dbpath)

   `sudo mongod --dbpath /usr/local/var/mongodb`

2. Then, generate data and store into your own local database.

   `python3 ratesPrep.py`

   > Possible error and solution: [ SSL: CERTIFICATE_VERIFY_FAILED error](https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org)

3. Next, run.

   `python3 project3.py`

### Explanations

- ratePrep.py: insert rates into mongodb.

> Currency data source: [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).
>
> Historical reference rates is read from csv file provided, and new rates updated everyday is based on [ECB's current reference rates xml](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml?55b6b6eeb6b3e8ec3a8da152d1d20c15).
