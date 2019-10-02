import pytest

from commands import login, wait_page_element, logout, get_page, set_text_to_element, set_value_to_element, \
    get_elem_by_class, wait_page_loaded
from config import LOGIN, PASSWORD
from testcases import *


@pytest.fixture(scope="function", params=[
    (first_test_case_values, first_test_case_texts, True),
    (second_test_case_values, second_test_case_texts, True),
    (third_test_case_values, third_test_case_texts, False)])
def get_case(request):
    """

    :param request: ТестовыеДанные/ОжидаемыйРезультат
    :return:

        Создаю набор тестовых данных
    """
    return request.param


def test_create_bug(get_case):
    """

    :param get_case: Получение тестовых данных и ожидаемого результата
    :return:

        Тест создания ошибки с разными входными данными

        Получаю тестовые данные
        Заходу на сервер под существующей учетной записью
        Ожидаю элемент, существующий на авторизированной странице
            FIX: не самое лучшее решение
        Заполняю поля в форме ввода данных
        Нахожу и эмулирую нажатие кнопки сохранения
        Сохраняю результат тестирования
        Удаляю cookie данные для следующего теста
        Закрываю браузер для последующего чистого открытия с новым набором данных

    """
    (case_values, case_texts, result) = get_case
    firefox = login("http://localhost/login_page.php", LOGIN, PASSWORD)
    wait_page_element(firefox, "navbar", 5)
    firefox = get_page(firefox, "http://localhost/bug_report_page.php")
    for key, val in case_values.items():
        set_value_to_element(firefox, key, val)
    for key, val in case_texts.items():
        set_text_to_element(firefox, key, val)

    btn = get_elem_by_class(firefox, "btn-round")
    btn[0].click()
    try:
        wait_page_loaded(firefox, 5)
        if "Создать задачу - MantisBT" in firefox.title:
            test_result = False
        else:
            test_result = True
    except AssertionError:
        test_result = False
    logout(firefox)
    firefox.close()
    assert test_result == result
