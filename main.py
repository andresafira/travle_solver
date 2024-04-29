import pandas as pd
from math import inf
from typing import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


borders = pd.read_csv('GEODATASOURCE-COUNTRY-BORDERS.CSV')[['country_name', 'country_border_name']]


def get_borders(country) -> List[str]:
    return list(borders[borders['country_name'] == country]['country_border_name'])


def find_best_route(origin: str, destination: str) -> List[str]:
    node_info = dict()
    finished = list()
    in_analysis = list()

    in_analysis.append(origin)
    node_info[origin] = [0, None]

    while in_analysis:
        min_node = None
        min_dist = inf
        for node in in_analysis:
            if node_info[node][0] < min_dist:
                min_node = node
                min_dist = node_info[node][0]
        in_analysis.remove(min_node)
        if min_node == destination:
            break
        finished.append(min_node)

        for neighbor in get_borders(min_node):
            if neighbor in finished:
                continue
            alt_dist = node_info[min_node][0] + 1
            if neighbor not in in_analysis:
                in_analysis.append(neighbor)
                node_info[neighbor] = [alt_dist, min_node]
            elif alt_dist < node_info[neighbor][0]:
                node_info[neighbor] = [alt_dist, min_node]

    path = [destination]
    while path[0] is not origin:
        path.insert(0, node_info[path[0]][1])
    return path[1:-1]


def answer(url):
    driver = webdriver.Chrome()
    driver.get(url)
    title = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "title-text"))
    )
    origin, destination = title.text.replace("Today I'd like to go from ", '').split(' to ')
    driver.quit()

    path = find_best_route(origin, destination)
    print(path)


def answer_today():
    answer('https://travle.earth/')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        answer_today()
    elif len(sys.argv) == 2:
        answer(sys.argv[1])
    elif len(sys.argv) == 3:
        print(find_best_route(sys.argv[1].lower().capitalize(), sys.argv[2].lower().capitalize()))
    else:
        print('Invalid amount of parameters')
