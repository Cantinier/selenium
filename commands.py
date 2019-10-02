from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec


class Firefox(object):

    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_browser(self):
        return self.driver


browser = Firefox()


def wait_page_element(driver, elem_id, time):
    """
    :param driver: Объект - браузер
    :param elem_id: ID искомого элемента на странице
    :param time: Время ожидания вы секундах
    :return: Элемент страницы

        Ожидаю загрузку страницы с указанным таймаутом
        Произвожу поиск элемента по ID
        В случае отсутствия искомого элемента или превышения таймаута - вывожу AssertionError
    """
    try:
        element = WebDriverWait(driver, time)
        element = element.until(ec.presence_of_element_located((By.ID, elem_id)))
    except TimeoutException:
        assert False
    return element


def login(url, login, password):
    """
    :param url: Строка страницы авторизации
    :param login: Логин пользователя
    :param password: Пароль пользователя
    :return: Объект - браузер

        Попытка авторизации на сайте по переданным учетным данным и возврат браузера

        Получаю созданный при инициализации файла объект браузера и перехожу на страницу авторизации
        Ожидаю загрузку страницы с таймаутом в 5 сек
        Ввожу логин, перехожу на страницу ввода пароля, ввожу пароль
        Произвожу попытку логина и возвращаю результат в виде объекта браузера
    """
    firefox = browser.get_browser()
    firefox.get(url)
    login_elem = wait_page_element(firefox, "username", 5)
    login_elem.send_keys(login)
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
