from bs4 import BeautifulSoup
from requests import post

from database import UserData


def get_results(user_data: UserData) -> str:
    r = post('http://nscm.ru/giaresult/tablresult.php', {
        'Lastname': user_data.Lastname,
        'Name': user_data.Name,
        'SecondName': user_data.SecondName,
        'DocNumber': user_data.DocNumber
    })

    response = ''
    trs = BeautifulSoup(r.content, 'html.parser').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        exam_name = tds[0].get_text()
        exam_points = tds[2].get_text()
        exam_mark = tds[3].get_text()
        response += f'{exam_name}: {exam_mark} ({exam_points} баллов)\n'

    return response
