from datetime import datetime, timedelta
import platform
import sys
import logging

import aiohttp
import asyncio


BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="


async def request(url: str, session, currencies):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                result = await resp.json()
                return process_response(result, currencies)
            else:
                logging.error(f"Error status: {resp.status} for {url}")
    except aiohttp.ClientConnectorError as err:
        logging.error(f'Connection error: {url} {str(err)}')
        return 'Not found'
    

def process_response(result: dict, currencies):
    outcome = []
    if not result:
        return 'Not found'
    date = result['date']
    data = result['exchangeRate']
    currency_dict = {}
    for currency in currencies or ['USD', 'EUR']:
        currency_data = next(filter(lambda el: el["currency"] == currency.upper(), data), None)
        if currency_data:
            try:
                currency_dict[currency.upper()] = {'sale': currency_data['saleRate'], 'purchase': currency_data['purchaseRate']}
            except KeyError:
                currency_dict[currency.upper()] = 'Not available'
        else:
            currency_dict[currency.upper()] = 'No such currency found'
    outcome.append({date: currency_dict})
    return outcome


def get_links(days=None):
    urls = []
    today = datetime.now()
    work_URL = BASE_URL + today.strftime("%d.%m.%Y")
    if days is None:
        urls.append(work_URL)
    else:
        for _ in range(min(int(days), 10)):
            work_URL = BASE_URL + today.strftime("%d.%m.%Y")
            urls.append(work_URL)
            today -= timedelta(days=1)
    return urls


async def main(urls, currencies):
    async with aiohttp.ClientSession() as session:
        tasks = [request(url, session, currencies) for url in urls]
        results = await asyncio.gather(*tasks)
        return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    def_cur = ['USD', 'EUR']
    if len(sys.argv) > 1:
        currencies = (def_cur + sys.argv[2:]) if len(sys.argv) > 2 else def_cur
        results = asyncio.run(main(get_links(sys.argv[1]), currencies))
    else:
        results = asyncio.run(main(get_links(), def_cur))
    for item in results:
        for date in item:
            for key, value in date.items():
                print(key)
                print(value)
                print("-------------------")