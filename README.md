
# Travelnest take home test
The task for this take-home test was to:
* Scrape property name, type, number of bedrooms and bathrooms, and list amenities for a list of AirBnB property URLs, e.g.:
https://www.airbnb.co.uk/rooms/33571268
https://www.airbnb.co.uk/rooms/20669368
https://www.airbnb.co.uk/rooms/50633275
## Description of solution
### Basic summary
* The solution is written in Python, as I created a similar solution in JavaScript not long ago ([see here](https://github.com/luke-pomeroy/adimo-test)) and thought it would be interesting to use Python this time.
* asyncio is used so that functions can be run concurrently/asynchronously.
* as some of the data needed is inside a modal, and this is not in the DOM upon render playwright is used as a headless browser.
* BeautifulSoup is used to parse and scrape data from the HTML returned.
* There are some basic test cases that can be run also.
* When scraping is complete, results are saved as JSON in a file called output.json.
### Challenges
* It looks like AirBnB uses dynamic class names, so selecting elements is not always straightforward.
* It's likely that AirBnB has rate limiting, and a WAF to detect scraping so our IP is likely to be blocked after a while.
* We need to check if AirBnB is redirecting us because the property no longer exists.
### Further ideas/solutions
* The DOM selectors used with BeautifulSoup are hard-coded. It would be better to have these as variables (or in a database for example) so we can easily change them when AirBnB inevitably changes their page structure.
* We may want to expand the solution to cover other types of booking website.
* It might be good to setup rotating proxies, so that we can avoid our IP being blocked. 
* The functions are all in one file; if I had more time I would have made this a bit more modular.
* The test cases are fairly basic and could be expanded further.
* There isn't really any error handling in the functions. Although it works, there are likely edge cases we will come across when handling a larger number of URLs.
* Some of the functions could do with further refinement / refactoring.
* Performance could be further improved by using multiprocessing in addition to asyncio.

### Dependencies
* [Python3.12+](https://www.python.org/)
* [Pytest](https://docs.pytest.org/) - testing framework
* [Playwright](https://playwright.dev/) - headless browser
* [Asyncio](https://docs.python.org/3/library/asyncio.html) - async functionality
### Installation
Create a virtual environment:
```
python -m venv venv
```
Activate the virtual environment:
```
. venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt 
```
To run the tests:
```
pytest
```
To run the scraper:
```
python main.py
```
An 'output.json' file will be created containing the results.
