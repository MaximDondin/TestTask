import requests
import datetime
import time

def get_response():
    url = "https://yandex.com/time/sync.json?geo=213"
    response = requests.get(url)
    data = response.json()
    return data, response


def show_inf():
    response = get_response()
    print(f'a) Сырой ответ: \n{response[1].text}\n')

    time_sec = response[0]['time'] // 1000
    human_time = datetime.datetime.fromtimestamp(time_sec)
    print('b) значение времени в «человекопонятном» формате  и название временной зоны:')
    print('время -', human_time.strftime('%H:%M:%S'))
    print('временная зона -', response[0]['clocks']['213']['name'], response[0]['clocks']['213']['offsetString'], '\n')

def search_delta():
    delta = []
    for i in range(5):
        start_time = time.time()
        get_response_time = get_response()
        delta.append(get_response_time[0]['time'] / 1000 - start_time)

    print(f'c) дельта времени: \n{delta[0]}\n')
    print(f'd) средняя дельта: \n{sum(delta) / len(delta)}')

if __name__ == "__main__":
    show_inf()
    search_delta()