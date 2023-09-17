# TOPUS-shop
## навігація 
:bulb: [Ідея](#ідея) :bulb:

:computer: [Функціонал](#функціонал) :computer:

:warning: [Вимоги](#вимоги) :warning:

:black_nib: [Установка](#установка) :black_nib:

:question: [Що у планах](#що_у_планах) :question:

:books: [Джерела](#джерела)  :books:

:point_right: [Дякую](#дякую) :point_left:

:package: [Оновлення](#оновлення) :package:

## TOPUS-shop

__

<a name="ідея"></a>

## Идея

__

<a name="функціонал"></a>

## Функционал

__

<a name="вимоги"></a>

## Требования
- Python 3.9 и выше
- PostgreSQL 14+


<a name="Установка"></a>

## Установка

__

<a name="що у планах"></a>

## Що_у_планах

__

<a name="джерела"></a>

## Джерела

- https://www.youtube.com/@SeniorPomidorDeveloper


<a name="дякую"></a>

## Дякую

__

<a name="оновлення"></a>

## Оновлення

version 0.0.7
- Розроблена кастомна модель User
- Oновленні тести
- Добавленні djoser та jwt
- Добавленні базові templates
- Добавлений додаток users
- Реєстрація та логін користувача  (логін за email | username)
- Warnings - social_user() missing 1 required positional argument: 'uid'

version 0.0.6
- Добавленні нові поля для виводу в серіалізаторі "одягу"
- Добавлен серіалізатор для рейтингу, а також в admin.py за для запобігання створення дублюючих рейтингів
- Допрацьоване кешуюче поле рейтингу в головній моделі
- Добавленні тести для рейтингу

version 0.0.5
- Допрацьована робота генератора серійного номеру
- Нове /кєшуюче\ поле rating у mainmodel ( в розробці )
- Виправлені методи save в admin.py для інших моделей
- Добавлен файл test_utlis 

version 0.0.4
- Добавленні поля discount, viewed для mainmodel
- Добавленні annotaion для оптимізаціії sql запросів + тести

version 0.0.3
- Видалене поле slug для Mainmodel 
- Добавленні поля date_create | s_code
- Добавлен генератор серійного коду при створенні нового запису django-admin / postman
- Добавлена admin.model для Home
- WARNING в тестах -> DateTimeField MainModel.date_created received a naive datetime (2023-09-06 17:34:00) while time zone support is active.
- Початок розробки рейтингу для товарів

version 0.0.2
- Добавленні Permission
- Зміненні поля в моделях з null=True на blank=True

version 0.0.1
- Додана можливість аунтифікації через Google

version init
- Модели для одягу, ігрової переферії, товарів для дому
- тести для моделей (створення, фільтр, пошук)
