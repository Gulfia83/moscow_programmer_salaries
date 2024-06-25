import requests
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable


def get_hh_vacancies(language):
    vacancies_url = 'https://api.hh.ru/vacancies'
    area_id = '1'
    vacancies_per_page = '100'
    params = {
        'text': f'Программист {language}',
        'area': area_id,
        'per_page': vacancies_per_page,
    }
    all_vacancies = []
    page = 0
    while True:
        params['page'] = page
        response = requests.get(vacancies_url, params=params)
        response.raise_for_status()
        vacancy_descriptions = response.json()
        all_vacancies.extend(vacancy_descriptions['items'])
        if page >= vacancy_descriptions['pages'] - 1:
            break
        page += 1
    
    return all_vacancies, vacancy_descriptions['found']

def get_sj_vacancies(language, api_key):
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    start_page_number = 0
    city_name = 'Москва'
    vacancies_per_page = '100'

    headers = {'X-Api-App-Id': api_key}

    params = {
        'page': start_page_number,
        'town': city_name,
        'count': vacancies_per_page,
        'keyword': f'Программист {language}',
    }

    all_vacancies = []
    page = 0
    while True:
        params['page'] = page
        response = requests.get(vacancies_url, headers=headers, params=params)
        response.raise_for_status()
        vacancy_descriptions = response.json()
        all_vacancies.extend(vacancy_descriptions['objects'])
        if len(all_vacancies) >= vacancy_descriptions['total']:
            break
        page += 1

    return all_vacancies, vacancy_descriptions['total']
  
def predict_salary(payment_from, payment_to):
    if payment_to and payment_from:
        return (payment_from + payment_to) / 2

    elif payment_from == None:
        return payment_to * 0.8

    elif payment_to:
        return payment_from * 1.2

def predict_rub_salary_hh(salary):
    if salary == None or salary['currency'] != 'RUR':
        return None
    predicted_salary = predict_salary(salary['from'], salary['to'])
    return predicted_salary

def predict_rub_salary_sj(vacancy):
    predicted_salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
    return predicted_salary

def fetch_hh_average_programmer_salary(languages):
    hh_vacancies_salaries = {}
    for language in languages:
        vacancies, total_vacancies = get_hh_vacancies(language)

        salaries = []
        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_hh(vacancy['salary'])
            if predicted_salary:
                salaries.append(predicted_salary)

        average_salary = int(sum(salaries) / len(salaries)) if salaries else 0
        hh_vacancies_salaries[language] = {
            'vacancies_found': total_vacancies,
            'vacancies_processed': len(salaries),
            'average_salary': average_salary
        }

    return hh_vacancies_salaries

def fetch_sj_average_programmer_salary(languages, api_key):
    sj_vacancies_salaries = {}
    for language in languages:
        vacancies, total_vacancies = get_sj_vacancies(language, api_key)

        salaries = []
        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_sj(vacancy)
            if predicted_salary:
                salaries.append(predicted_salary)

        average_salary = int(sum(salaries) / len(salaries)) if salaries else 0 
        sj_vacancies_salaries[language] = {
            'vacancies_found': total_vacancies,
            'vacancies_processed': len(salaries),
            'average_salary': average_salary
        }

    return sj_vacancies_salaries

def print_table(vacancy_descriptions, title):
    table_data = [['Язык программирования', 'Вакансий найдено','Вакансий обработано', 'Средняя зарплата']]
    for language, stats in vacancy_descriptions.items():
        table_data.append([
          language, 
          stats['vacancies_found'], 
          stats['vacancies_processed'], 
          stats['average_salary'],
        ])

    table = AsciiTable(table_data, title)
    print(table.table)
  
def main():
    load_dotenv()
    languages = ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'C', 'PHP', 'Ruby']

    api_key = os.environ['SUPER_JOB_API_KEY']

    sj_average_programmer_salary = fetch_sj_average_programmer_salary(languages, api_key)
    hh_average_programmer_salary = fetch_hh_average_programmer_salary(languages)

    print_table(sj_average_programmer_salary, 'SuperJob Moscow')

    print_table(hh_average_programmer_salary, 'HeadHunter Moscow')

if __name__ == '__main__':
    main()


