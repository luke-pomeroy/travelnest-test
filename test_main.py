import pytest
import main

success_urls = [    
    'https://www.airbnb.co.uk/rooms/20669368',
    'https://www.airbnb.co.uk/rooms/50633275'
    ]

removed_urls = ['https://www.airbnb.co.uk/rooms/33571268']

@pytest.mark.asyncio
async def test_removed_page():
    result = await main.main(removed_urls)
    result_data = result[removed_urls[0]]
    assert type(result) == dict
    assert type(result_data) == dict
    assert result_data['status'] == 'not found'
    assert 'datetime' in result_data

@pytest.mark.asyncio
async def test_successful_scrape():
    result = await main.main(success_urls)
    result_data = result[success_urls[0]]
    assert type(result) == dict
    assert type(result_data) == dict
    assert result_data['status'] == 'success'
    assert 'datetime' in result_data
    assert 'name' in result_data
    assert 'type' in result_data
    assert 'bedrooms' in result_data
    assert 'bathrooms' in result_data
    assert 'amenityGroups' in result_data
    assert type(result_data['amenityGroups']) == list
