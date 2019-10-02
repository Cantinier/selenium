import pytest
from commands import login, wait_page_element, logout
from config import LOGIN


@pytest.fixture(scope="function", params=[
    ("Administrator", False),
    ("admin", True),
    ("IlonMask", True),
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
        Сохраняю результат тестирования
        Удаляю cookie данные для следующего теста
        Закрываю браузер для последующего чистого открытия с новым набором данных

    """
    (password, result) = get_pass
    firefox = login("http://localhost/login_page.php", LOGIN, password)
    try:
        wait_page_element(firefox, "navbar", 2)
        test_result = True
    except AssertionError:
        test_result = False
    logout(firefox)
    firefox.close()
    assert test_result == result
