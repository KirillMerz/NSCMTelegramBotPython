from bs4 import BeautifulSoup
from requests import post

from database import UserData


def get_results(user_data: UserData) -> str:
    response = ''

    r = post('http://nscm.ru/giaresult/tablresult.php', {
        'Lastname': user_data.Lastname,
        'Name': user_data.Name,
        'SecondName': user_data.SecondName,
        'DocNumber': user_data.DocNumber,
    })

    tbody = BeautifulSoup(r.content, 'html.parser').find('tbody')
    for tr in tbody.find_all('tr'):
        tds = tr.find_all('td')
        exam_name = tds[0].get_text()
        exam_mark = tds[3].get_text()
        response += f'{exam_name}: {exam_mark}\n'

    return response
