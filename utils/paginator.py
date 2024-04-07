import math

# Простой пагинатор
from typing import Optional


class Paginator:
    def __init__(self, array: Optional[list], page: int = 1, per_page: int = 1):
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        # math.ceil - округление в большую сторону до целого числа
        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self):
        if self.page != 0:
            start = (self.page - 1) * self.per_page
            stop = start + self.per_page
            return self.array[start:stop]
        else:
            start = self.pages - 1
            stop = self.pages
            return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def get_next(self):
        return self.page + 1 if self.page != self.pages else 1

    def get_previous(self):
        return self.page - 1 if self.page != 1 else self.pages
