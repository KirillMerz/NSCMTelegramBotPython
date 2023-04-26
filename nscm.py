from bs4 import BeautifulSoup
import aiohttp

from database import UserData


async def get_results(user_data: UserData) -> str:
    results = await _get_results(user_data)

    if 'не найдены'.encode('UTF-8') in results:
        return 'Учетные данные были введены неверно, результаты не найдены'

    response = ''

    trs = BeautifulSoup(results, 'html.parser').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        exam_name = tds[0].get_text()
        exam_points = tds[2].get_text()
        exam_mark = tds[3].get_text()
        response += f'{exam_name}: {exam_mark} ({exam_points} баллов)\n'

    return response


async def _get_results(user_data: UserData) -> bytes:
    request = aiohttp.request('post', 'http://nscm.ru/giaresult/tablresult.php', data = {
        'Lastname': user_data.Lastname,
        'Name': user_data.Name,
        'SecondName': user_data.SecondName,
        'DocNumber': user_data.DocNumber
    })

    async with request as r:
        return await r.read()

