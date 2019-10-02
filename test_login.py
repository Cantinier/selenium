import pytest
from commands import login, wait_page_element, logout
from config import LOGIN


@pytest.fixture(scope="function", params=[
    ("Administrator", False),
    ("12345", False),
    ("IlonMask", False),
    ("admin", True),
    ("admin0303", False),
    ("admin", True)])
def get_pass(request):
    """

    :param request: Очередная пара Пароль:ОжидаемыйРезультат
    :return:

        Создаю набор тестовых данных
    """
    return request.param


def test_login(get_pass):
    """

    :param get_pass: Получение очередной пары Пароль:ОжидаемыйРезультат
    :return:

        Тест авторизации пользователя под различными паролями

        Получаю очередную связку Пароль:ОжидаемыйРезультат
        Произвожу попытку логина под логином Administrator и очередным паролем
        Ожидаю элемент, существующий на авторизированной странице
            FIX: не самое лучшее решение
        Удаляю cookie данные для следующего теста
        Сохраняю результат тестирования
    """
    (password, result) = get_pass
    firefox = login("http://localhost/login_page.php", LOGIN, password)
    try:
        wait_page_element(firefox, "navbar", 2)
        test_result = True
    except AssertionError:
        test_result = False
    logout(firefox)
    assert test_result == result


