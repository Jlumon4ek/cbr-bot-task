import aiohttp
import xml.etree.ElementTree as ET
import redis.asyncio as aioredis
import asyncio
import loguru
import sys

async def fetch_currencies():
    loguru.logger.info("Fetching currencies...")
    async with aiohttp.ClientSession() as session:
        async with session.get('https://cbr.ru/scripts/XML_daily.asp') as response:
            xml_data = await response.text()
            root = ET.fromstring(xml_data)
            for valute in root.findall('Valute'):
                num_code = valute.find('NumCode').text
                char_code = valute.find('CharCode').text
                name = valute.find('Name').text
                vunit_rate = valute.find('VunitRate').text if valute.find('VunitRate') is not None else "N/A"
            
                data = {
                    'num_code': num_code,
                    'char_code': char_code,
                    'name': name,
                    'vunit_rate': vunit_rate
                }

                redis = aioredis.from_url("redis://redis")
                key = f"currency:{data['char_code']}"
                await redis.hset(key, mapping=data)

    loguru.logger.info("Currencies fetched successfully")

async def get_all_currencies():
    loguru.logger.info("Getting all currencies...")
    redis = aioredis.from_url("redis://redis")
    keys = await redis.keys("currency:*")
    currencies = []
    for key in keys:
        raw_data = await redis.hgetall(key)
        formatted_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in raw_data.items()}
        formatted_data['num_code'] = int(formatted_data['num_code'])
        formatted_data['vunit_rate'] = float(formatted_data['vunit_rate'].replace(',', '.')) if 'vunit_rate' in formatted_data else None
        currencies.append(formatted_data)
    return currencies


async def get_currency(char_code: str):
    loguru.logger.info(f"Getting currency {char_code}...")
    redis = aioredis.from_url("redis://redis")
    key = f"currency:{char_code}"
    raw_data = await redis.hgetall(key)
    formatted_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in raw_data.items()}
    formatted_data['num_code'] = int(formatted_data['num_code'])
    formatted_data['vunit_rate'] = float(formatted_data['vunit_rate'].replace(',', '.')) if 'vunit_rate' in formatted_data else None
    return formatted_data

async def fetch_currencies_periodically():
    loguru.logger.info("Fetching currencies periodically...")
    while True:
        await fetch_currencies()
        await asyncio.sleep(43200)
