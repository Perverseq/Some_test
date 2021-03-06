from behave import *
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


@when("Получили имя канала из файла channel.txt")
def step_impl(context):
    with open(os.path.abspath("channel.txt"), "r") as channel_name_f:
        context.channel_name = channel_name_f.readline()


@step("Проверили пустой был файл channel.txt или нет")
def step_impl(context):
    context.driver.get("http:\\youtube.com\\" + context.channel_name)
    if context.driver.title == "YouTube":
        context.driver.save_screenshot(os.path.abspath("Screens\\empty_channel.jpg"))
        print("Вы не ввели имя канала\n")
        send_msg(context, os.path.abspath('Screens\\empty_channel.jpg'), 'Вы не ввели имя канала в channel.txt')
        context.scenario.skip(require_not_executed=True)
    else:
        print("Файл не пустой\n")


@step("Проверили существует такой канал или нет")
def step_impl(context):
    context.driver.get("http:\\youtube.com\\" + context.channel_name)
    if context.driver.title == "404 Not Found":
        context.driver.save_screenshot(os.path.abspath("Screens\\invalid_channel.jpg"))
        print("Такого канала не существует\n")
        send_msg(context, os.path.abspath('Screens\\invalid_channel.jpg'), 'Такого канала не существует.')
        context.scenario.skip(require_not_executed=True)
    else:
        print("Канал существует\n")


@step("Зашли на этот канал на ютубе")
def step_impl(context):
    context.driver.get("http:\\youtube.com\\" + context.channel_name)


@then('Спарсили количество подписчиков в файл, сделали скриншот')
def step_impl(context):
    element = context.driver.find_element_by_xpath('//*[@id="subscriber-count"]')
    name_channel = str(context.driver.find_element_by_id("channel-title").text)
    subs_yet = str(element.text)
    with open(".//Subs.txt", "a") as subs_count:
        subs_count.write("На канале {0} {1} {2}.\n".format(name_channel, subs_yet, datetime.now()))
        context.driver.save_screenshot(os.path.abspath("Screens\\{}.jpg".format(subs_yet)))
    send_msg(context, os.path.abspath("Screens\\{}.jpg".format(subs_yet)), 'Все шаги прошли успешно.')


@step("Обновили страницу")
def step_impl(context):
    context.driver.refresh()


@then('Подождали "{minutes}" минут(-ы)')
def step_impl(context, minutes):
    time.sleep(float(minutes) * 60)


@then("Поставили видео на паузу")
def step_impl(context):
    try:
        context.driver.find_element_by_xpath('//*[@aria-label="Пауза"]').click()
    except NoSuchElementException:
        print("На главной странице нет автоматически запускающегося видео\n")


def send_msg(context, path, txt):
    login = context.logpass[0]
    password = context.logpass[1]
    subj = context.subj
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(login , password)
    msg = MIMEMultipart()
    image = MIMEApplication(open(path, 'rb').read())
    image.add_header('Content-Disposition', 'attachment', filename=path)
    msg.attach(image)
    text = MIMEText(txt)
    msg.attach(text)
    server.sendmail(login, subj, msg.as_string())
    server.quit()
    os.remove(path)
