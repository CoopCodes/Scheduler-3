import requests
import random

from pprint import pprint


def login(mail, password):
    s = requests.Session()
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ] 
    
    headers = {
        "User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]}

    payload = {
        'email': mail,
        'password': password,
    }
    res = s.post('https://goldcoast.cs.adventist.edu.au/#?page=/timetable',
                headers=headers, data=payload)
    print(res.content)
    return s

password = "asdfghjkl;'"
session = login('gc021217@goldcoastcc.qld.edu.au', password)
r = session.get(
    'https://goldcoast.cs.adventist.edu.au/seqta/student/load/timetable')
pprint(r.content)
