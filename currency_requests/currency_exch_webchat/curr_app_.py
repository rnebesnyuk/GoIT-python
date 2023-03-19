from datetime import datetime, timedelta
import platform
import logging

import aiohttp
import asyncio
import websockets
import names
from aiofile import async_open
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK


BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="
def_cur = ['USD', 'EUR']


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
            currency_dict[currency.upper()] = 'Not found'
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


async def get_exchange(urls, currencies):
    async with aiohttp.ClientSession() as session:
        tasks = [request(url, session, currencies) for url in urls]
        results = await asyncio.gather(*tasks)
        return results
    

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def handle_exchange(self, message: str, ws: WebSocketServerProtocol):
        days = message.split(" ")
        if len(days) == 1:
            exc = await get_exchange(get_links(), def_cur)
        else:
            exc = await get_exchange(get_links(int(days[1])), def_cur)
        # async with async_open('file.txt', 'a+', encoding='utf-8') as afp:
        #     await afp.write(f'{ws.remote_address} called "exchange" command\n')
        return str(exc)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith('exchange'):
                exc = await self.handle_exchange(message, ws)
                await self.send_to_clients(exc)
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def server_start():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)    
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(server_start())
