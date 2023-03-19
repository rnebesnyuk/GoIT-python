from datetime import datetime, timedelta
import platform
import sys

import aiohttp
import asyncio


BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="


async def request(url: str, session):
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    outcome = []
                    date_ = {}
                    totaldict = {}
                    currency = {}
                    if result:
                        date = result['date']
                        data = result['exchangeRate']
                        curr1, = list(filter(lambda el: el["currency"] == 'USD', data))
                        curr2, = list(filter(lambda el: el["currency"] == 'EUR', data))
                        currency['sale'] = curr1['saleRate']
                        currency['purchase'] = curr1['purchaseRate']
                        totaldict[curr1['currency']] = currency
                        currency = {}
                        currency['sale'] = curr2['saleRate']
                        currency['purchase'] = curr2['purchaseRate']
                        totaldict[curr2['currency']] = currency
                        date_[date] = totaldict
                        outcome.append(date_)
                        return outcome
                    return 'Not found'
                else:
                    print(f"Error status: {resp.status} for {url}")
        except aiohttp.ClientConnectorError as err:
            print(f'Connection error: {url}', str(err))

 
def get_links(days=None):
    urls = []
    today = datetime.now()
    work_URL = BASE_URL + today.strftime("%d.%m.%Y")
    if days == None:
        urls.append(work_URL)
    else:
        for _ in range((int(days)), 10):
            work_URL = BASE_URL + today.strftime("%d.%m.%Y")
            urls.append(work_URL)
            today = today - timedelta(days=1)
    return urls



async def main(urls):
    async with aiohttp.ClientSession() as session:
        result = [request(url, session) for url in urls]
        return await asyncio.gather(*result)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if len(sys.argv) > 1:
        r = asyncio.run(main(get_links((sys.argv[1]))))
        print(r)
    else:
        r = asyncio.run(main(get_links()))
        print(r)