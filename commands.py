from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec


class Firefox(object):

    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_browser(self):
        return self.driver


def wait_page_loaded(firefox, time):
    """
    :param firefox: Объект - браузер
    :param time: таймаут
    :return: Объект - браузер

        Ожидание окончания загрузки текущей страницы с отстрелом по таймауту
    """
    try:
        WebDriverWait(firefox, time).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
    except TimeoutException:
        assert False
    return firefox


def wait_page_element(firefox, elem_id, time):
    """
    :param firefox: Объект - браузер
    :param elem_id: ID искомого элемента на странице
    :param time: Время ожидания вы секундах
    :return: Элемент страницы

        Ожидаю загрузку страницы с указанным таймаутом
        Произвожу поиск элемента по ID
        В случае отсутствия искомого элемента или превышения таймаута - вывожу AssertionError
    """
    try:
        element = WebDriverWait(firefox, time)
        element = element.until(ec.presence_of_element_located((By.ID, elem_id)))
    except TimeoutException:
        assert False
    return element


def login(url, user_login, password):
    """
    :param url: Строка страницы авторизации
    :param user_login: Логин пользователя
    :param password: Пароль пользователя
    :return: Объект - браузер

        Попытка авторизации на сайте по переданным учетным данным и возврат браузера

        Создаю объект браузера и перехожу на страницу авторизации
        Ожидаю загрузку страницы с таймаутом в 5 сек
        Ввожу логин, перехожу на страницу ввода пароля, ввожу пароль
        Произвожу попытку логина и возвращаю результат в виде объекта браузера
    """
    browser = Firefox()
    firefox = browser.get_browser()
    firefox.get(url)
    login_elem = wait_page_element(firefox, "username", 5)
    login_elem.send_keys(user_login)
    login_elem.send_keys(Keys.RETURN)
    wait_page_element(firefox, "password", 5)
    password_elem = firefox.find_element_by_name("password")
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.RETURN)
    return firefox


def logout(firefox):
    """
    :param firefox: Объект-браузер
    :return:

        Сбрасываю cookie для выхода из учетной записи
    """
    firefox.delete_all_cookies()


def get_page(firefox, url):
    """
    :param firefox:  Объект-браузер
    :param url: Ссылка
    :return: Объект-браузер

        Ожидается загрузка указанного адреса и возвращается браузер
    """
    firefox.get(url)
    wait_page_loaded(firefox, 5)
    return firefox


def get_elem_by_class(firefox, classname):
    """
    :param firefox: Объект-браузер
    :param classname: Название класса
    :return: Элемент
        Находит элемент по названию класса
    """
    element = firefox.find_elements_by_class_name(classname)
    return element


def set_value_to_element(firefox, element, value):
    """
    :param firefox: Объект-браузер
    :param element: Элемент страницы
    :param value: Значение
    :return:

        Устанавливает элементу указанное значение

    """
    element = Select(wait_page_element(firefox, element, 5))
    element.select_by_value(value)


def set_text_to_element(firefox, element, text):
    """
    :param firefox: Объект-браузер
    :param element: Элемент страницы
    :param text: Текст
    :return:

            Передает в элемент указанный текст
                # FIX необходимо добавить обработку события на неподдерживаемые типы элементов
    """
    element = wait_page_element(firefox, element, 5)
    element.send_keys(text)
