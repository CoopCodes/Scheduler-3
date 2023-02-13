import requests
from bs4 import BeautifulSoup

def get_problem(problem_num):
    # The URL of the problem you want to scrape
    url = f'https://projecteuler.net/problem={problem_num}'

    # Send a request to the website
    response = requests.get(url)

    # Parse the HTML of the website
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the element containing the problem statement
    problem_div = soup.find('div', class_='problem_content')

    # Extract the text of the problem statement
    problem = problem_div.get_text()

    # Print the problem statement
    return problem + f'\n{url}'

if __name__ == "__main__":
    get_problem(1)