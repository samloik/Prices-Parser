import enum

class SeleniumNextPageTypes(enum.Enum):
    # пока кнопка дальше не исчезнет
    NEXT_BUTTON_ABSENT = 1,
    # пока не появится web элемент последней страницы
    NEXT_BUTTON_TO_STOP_ELEMENT = 2
