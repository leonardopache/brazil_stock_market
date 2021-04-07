# Brazilian stock list #

The goal of this project is retrieve from the stock exchange a list of REIT's and Common equity available in Brasil. 
For that is used a sequence of scraper to identify the companies listed and create a historical data in CSV files.


### What is this repository for? ###

* Create a local historical data from stock trade to apply algorithms of Quantitative Trading. 
* v0.1

### How do I get set up? ###

* Setup it locally:
  - Checkout the source code;
  - How to compile and install the package:
    - from home of project, generate the compiled structure. build/, dist/ and xxx.egg.info.
       ```
       python setup.py bdist_wheel
       ```
    - if everything ok, install the .whl file in dist/
      ```
      python -m pip install dist/xxx-0.1-py3-none-any.whl
      ```
  ...or add ***brazil_stock_market==0.1*** in requirements.txt
* Usage, this package can be executed as background Job by the OS cron
  - To get company information: (ideally exec once a week of month)
  ``` 
  MarketDataScraper.scraper_market_information()
  ```
  
  - To update the trading historic: (ideally exec every day after the market close)
  ```
  MarketDataScraper.update_series_data()
  ```
  - ex osx.:
    - Exec every first day of the month
    ```
    (0 0 1 * *) : python -c "from brazil_stock_market.company_scraper.run_scraper import MarketDataScraper; MarketDataScraper.scraper_market_information()"  >> ~/log_bra_sm.txt
    ```
    - Exec every day of week at midnight
    ```
    (0 0 * * 1-5) : python -c "from brazil_stock_market.company_scraper.run_scraper import MarketDataScraper; MarketDataScraper.update_series_data()"  >> ~/tmp/log_bra_sm.txt
    ```
* Dependencies
  - look for requirements.txt 
* How to run tests
  - not implemented 
  
### What are coming next? ###
- [ ] suggestions ??

### Who do I talk to? ###

* leonardo pache
* https://github.com/leonardopache