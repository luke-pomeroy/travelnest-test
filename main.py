import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import json
import datetime

tz = datetime.timezone.utc
dt = datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:%S%z')

urls_to_scrape = [
    'https://www.airbnb.co.uk/rooms/33571268',
    'https://www.airbnb.co.uk/rooms/20669368',
    'https://www.airbnb.co.uk/rooms/50633275'
]

def extract_amenities(amenity_list):
    amenities = []
    for amenity in amenity_list:
        group_title = amenity.div.h3.get_text()
        group_items = amenity.select('ul > li')
        group_amenities = []

        for item in group_items:
            details = item.select('div > div:nth-of-type(2) > div')
            if len(details) > 1:
                group_amenities.append({
                    'title': details[0].get_text(),
                    'available': True,
                    'description': details[1].get_text(),
                })
                continue

            unavailable = details[0].find('del')
            if unavailable:
                group_amenities.append({
                    'title': unavailable.get_text(),
                    'available': False
                })
                continue

            group_amenities.append({
                'title': details[0].get_text(),
                'available': True
            })
        amenities.append({
            'title': group_title,
            'amenities': group_amenities
        })
    return amenities

def extract_property_details(soup):
    property_name = soup.h1.get_text()
    property_type = soup.h2.get_text().split(' in ')[0]
    bedrooms = soup.select('section > div > ol > li:nth-of-type(2)')[0].get_text()[3]
    bathrooms = soup.select('section > div > ol > li:nth-of-type(4)')[0].get_text()[3]
    amenity_dialog = soup.select('div[aria-label="What this place offers"]')
    amenity_list = amenity_dialog[0].select('section > div:nth-of-type(2) > div')
    amenities = extract_amenities(amenity_list)

    return {
        'status': 'success',
        'datetime': dt,
        'name': property_name,
        'type': property_type,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'amenityGroups': amenities
    }

async def get_html(context, url):
    page = await context.new_page()
    response = await page.goto(url, timeout=600000)
    #Check if response is ok
    if not response.ok:
        return { 
            'status': 'not found',
            'datetime': dt
        }
    
    await page.wait_for_selector('body')
    #Click cookies button if visible
    if await page.query_selector('button:text-matches("OK")') != None:
        await page.locator('button:text-matches("OK")').click()
    #Click show all amenities button and wait for dialog
    await page.get_by_role('button', name='amenities').click()
    await page.wait_for_selector('div[aria-label="What this place offers"]')

    html = await page.inner_html('body')
    soup = BeautifulSoup(html, 'html.parser')
    result = extract_property_details(soup)
    await page.close()

    return result

async def open_pages(context, urls):
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_html(context, url)))
    results = await asyncio.gather(*tasks)
    return dict(zip(urls, results))

def output_to_json_file(json_text):
    f = open("output.json", "w")
    f.write(json_text)
    f.close()

async def main(urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        data = await open_pages(context, urls)
        await browser.close()
    pretty_json = json.dumps(data, indent=4) 
    output_to_json_file(pretty_json)
    return data

if __name__ == "__main__":
    asyncio.run(main(urls_to_scrape))

