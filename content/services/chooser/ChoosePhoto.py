"""Модуль выбора фотографии."""

import csv
from dataclasses import dataclass
from typing import List


@dataclass
class ChoosePhotoCSV:
    """Класс выбора фотографий из csv файла."""

    categories: List[str]

    def check_categories_number(self) -> bool:
        """Проверка колличества категорий."""
        return 0 <= len(self.categories) <= 10

    def get_allowed_urls(self) -> List[dict]:
        """Получение доступных для отображения url."""
        with open('test_data.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            allowed_urls = []
            unique_url = []
            last_url_status = False
            for row in reader:
                url, needed_amount_of_shows, image_categories = \
                    self.get_image_data(row)
                unique_url.append({
                            'url': url,
                            'needed_amount_of_shows': needed_amount_of_shows})

                # Проверка на совпадение категорий
                if self.check_matching_categories(image_categories):
                    # Механизм, который уменьшает вероятность выдачи одной
                    # и той же картинки несколько раз подряд
                    if self.check_last_url(url):
                        allowed_urls.append(
                            {'url': url,
                             'needed_amount_of_shows': needed_amount_of_shows})
                    else:
                        last_url_status = True
                        last_url = {
                            'url': url,
                            'needed_amount_of_shows': needed_amount_of_shows}
        if len(allowed_urls) == 0:
            if last_url_status:
                allowed_urls.append(last_url)
            else:
                allowed_urls = unique_url
        return allowed_urls

    def check_last_url(self, url: str) -> bool:
        """Проверка на совпадение с последним отображенным url."""
        with open('last_url.txt', 'r') as f:
            last_url = f.read()

        with open('last_url.txt', 'w') as f:
            f.write(url)

        return url != last_url

    def check_matching_categories(self, image_categories: List[str]) -> bool:
        """Проверка на совпадение категорий."""
        for image_category in image_categories:
            if image_category in self.categories:
                return True
        return False

    def get_image_data(self, row: dict) -> (str, int, list):
        """Получение данных избражения из строки csv файла."""
        categories = []
        url = ''
        needed_amount_of_shows = 0
        for key in row:
            if key == 'needed_amount_of_shows':
                needed_amount_of_shows = row[key]
            elif key == 'url':
                url = row[key]
            elif ('category' in key) and (row[key] != ''):
                categories.append(row[key])
        return url, needed_amount_of_shows, categories

    def get_next_url(self) -> str:
        """Получение следующего url."""
        allowed_urls = self.get_allowed_urls()
        next_url = ''
        max_count = 0
        # Механизм, позволяющий минимизировать вероятность возникновения
        # случаев, когда подходящие картинки уже исчерпали свой лимит и
        # ответить на запрос нечем.
        # Вызывается картинка с максимальным needed_amount_of_shows
        # Учет повтора картинки будет происходить если needed_amount_of_shows
        # совпадет у новой и старой картинки
        for url in allowed_urls:
            needed_amount_of_shows = int(url['needed_amount_of_shows'])
            if int(url['needed_amount_of_shows']) > max_count:
                next_url = url['url']
                max_count = needed_amount_of_shows
        if max_count == 0:
            raise ValueError
        return next_url

    def write_csv(self, next_url) -> None:
        """Изменение needed_amount_of_shows в csv файле."""
        lines_csv = []
        with open('test_data.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            fieldnames = reader.fieldnames
            for row in reader:
                image_data = dict(row)
                if image_data['url'] == next_url:
                    image_data['needed_amount_of_shows'] = \
                        int(image_data.get('needed_amount_of_shows')) - 1
                lines_csv.append(image_data)
        with open('test_data.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter='\t',
                                    fieldnames=fieldnames)

            writer.writeheader()
            for line_csv in lines_csv:
                writer.writerow(line_csv)


def get_next_url(categories: List[str]) -> str:
    """Получение следующего url."""
    choose = ChoosePhotoCSV(categories)
    if choose.check_categories_number():
        try:
            next_url = choose.get_next_url()
        except ValueError:
            next_url = 'http://localhost:8000/static/error.jpg'
        else:
            choose.write_csv(next_url)
    else:
        next_url = 'http://localhost:8000/static/error.jpg'
    return next_url
