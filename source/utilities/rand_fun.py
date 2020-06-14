import numpy as np
import string
from datetime import datetime, timedelta


def random_word(word_length=11):
    return ''.join(np.random.choice(alphabet, size=word_length))


def random_string(num_of_words=3):
    res = ''
    for _ in range(num_of_words):
        res += ' ' + (random_word(np.random.randint(1, 11)))
    return res


def random_float(min_f=0.0, max_f=100000):
    return round(np.random.uniform(min_f, max_f), 2)


def random_date(year_display=99.0):
    return (datetime.today() - timedelta(days=np.random.randint(0, 365 * year_display))).date()


def random_employee():
    return random_word(np.random.randint(2, 7)), random_word(np.random.randint(2, 11)), random_date(10), np.random.choice(gender), \
           random_date(65)


def random_salary(empno):
    return {
        'empno': empno,
        'salary': random_float(30000, 10000),
        'fromdate': random_date(0.083),
        'todate': datetime.now().date(),
        'commentary': random_string(5)
    }


def random_titles(empn):
    if len(titles_rank) == 0:
        selected_title = np.random.choice(titles_ordinary)
    else:
        selected_title = np.random.choice(titles_rank)
        titles_rank.pop()
    return {
        'empno': empn,
        'title': selected_title,
        'fromdate': random_date(0.083),
        'todate': datetime.now().date(),
        'lotterychance': random_float(0, 1),
        'description': random_string(4)
    }


# Creating list of ASCII symbols to chose symbols from it
alphabet = np.array(list(string.ascii_lowercase))
# Creating list of titles and genders
titles_rank = ['president', 'director', 'head of management', 'ceo']
titles_ordinary = ['worker', 'manager', 'IT']
gender = ['M', 'F']
