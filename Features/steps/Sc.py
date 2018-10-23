from behave import *
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from PIL import ImageGrab


@when("Получить имя канала из файла channel.txt")
def step_impl(context):
    with open(".//channel.txt", "r") as channel_name_f:
        context.channel_name = channel_name_f.readline()


@step("Зайти на этот канал на ютубе, если канала нет, сделать скриншот")
def step_impl(context):
    context.driver.get("http:\\youtube.com\\" + context.channel_name)
    if context.driver.title == "404 Not Found":
        screen = ImageGrab.grab()
        screen.save(".\\Screens\\invalid_channel.jpg")
        skip_sc(context)
    else:
        pass


@step("Развернуть браузер на весь экран")
def step_impl(context):
    context.driver.maximize_window()





@then('Спарсить количество подписчиков в файл')
def step_impl(context):
    element = context.driver.find_element_by_xpath('//*[@id="subscriber-count"]')
    name_channel = str(context.driver.find_element_by_id("channel-title").text)
    subs_yet = str(element.text)
    with open(".//Subs.txt", "a") as subs_count:
        subs_count.write("На канале {0} {1} {2}.\n".format(name_channel, subs_yet, datetime.now()))
    screen = ImageGrab.grab()
    screen.save(".\\Screens\\{}.jpg".format(subs_yet))


@step("Обновить страницу")
def step_impl(context):
    context.driver.refresh()


@then('Подождать "{minutes}" минут(-ы)')
def step_impl(context, minutes):
    time.sleep(float(minutes) * 60)


@then("Поставить видео на паузу")
def step_impl(context):
    try:
        context.driver.find_element_by_xpath('//*[@aria-label="Пауза"]').click()
    except NoSuchElementException:
        pass


def skip_sc(context):
    context.scenario.skip(require_not_executed=True)

