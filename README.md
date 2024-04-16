# Travelnest take home test

This is my response to the Travelnest take home test, written in Python.

## Task Summary
Please write some code that scrapes property name, property type (e.g Apartment), number of bedrooms, bathrooms and list of the amenities for the following 3 properties:

https://www.airbnb.co.uk/rooms/33571268
https://www.airbnb.co.uk/rooms/20669368
https://www.airbnb.co.uk/rooms/50633275

This can be implemented in any language you prefer. Please put your project into a code repository and share it with us. Note that some of these URLs may not actually show property details – please handle this case appropriately.

## Initial Observations
- We can write this in any language - there are two approaches that I have used before, each with their own pros and cons:
    - Using Python and BeautifulSoup4 with Requests (we can also use headless browser like Playright)
    - Using Node/JavaScript and Cherio with Fetch or Axios (we can also use headless browser Puppeteer or Playright)
- I chose to use Python for this task, as I did the same with Node/JS a few months ago and it's fun to try out a new challenge!
- We can use pandas to create a DataFrame to contain the scraped data, then save it to a json file

- Challenges:
    - The class names of the elements we need to extract look random and probably rotate
    - We may need to extract the elements based on their style
    - Large companies like this will have defences from scrapers: a quick google shows that AirBnB uses these. They probably:
        - Have request rate limits
        - Possibly use honeypots (as we're only scraping one page without clicking links, shouldn't be an issue)
        - Use bot detection of some form
        - Are using a WAF and our IP is likely to get blocked after a while
    - So we may need to use one or more proxies to rotate our IP
    - May need to send a fake user agent with requests
    - We may need to rate limit requests but as only 3 links should be fine for now
    - We want this to be performant so should use async functions

- We need a test suite to check that:
    - Data is correctly recorded


## Elements to extract / data to record
- Status: found or not found
- Property Name: first title at the top of page - h1 element
- Propery type: first part of the second title, upto ' in ' - h2 element
- Number of bedrooms: below the second title, second li element in div > ol
- Bathrooms: below second title, last li in div > ol
- List of amenities: requires click on Show More and is not in the DOM until clicked
    - Button with text 'Show all N amenities'
    Dialogue with:
    - Amenity category (h3)
    - ul > li with each amenity - div > div > div[2nd] > two divs with amenity name and description (if no description only 1 inner div)


property name, property type (e.g Apartment), number of bedrooms, bathrooms and list of the amenities