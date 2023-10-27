# TOPUS-shop
## навігація 
:bulb: [Ідея](#ідея) :bulb:

:computer: [Функціонал](#функціонал) :computer:

:warning: [Вимоги](#вимоги) :warning:

:black_nib: [Встановлення](#встановлення) :black_nib:

:question: [Що у планах](#що_у_планах) :question:

:books: [Джерела](#джерела)  :books:

:point_right: [Дякую](#дякую) :point_left:

:package: [Оновлення](#оновлення) :package:

## TOPUS-shop

__


## Ідея

__


## Функціонал

__


## Вимоги
- Python >= 3.9
- PostgreSQL 14+



## Встановлення

__


## Що_у_планах

__


## Джерела

- https://www.youtube.com/@SeniorPomidorDeveloper
- https://www.youtube.com/@CodeWithClinton
- https://www.youtube.com/@geekyshows



## Дякую

- [ImDeath](mailto:hiphoplands@gmail.com) - Front-end (css | html)
- [vladfraer1](mailto:vladfraer1@gmail.com) - images | logo 


## Оновлення

version 0.1.6
- Нові моделі Order / Customer
- Готовий функціонал кошика з підтвердженням обраного
- Оплата через гугл / при отриманні


version 0.1.5
- Додані нові поля для Profile
- Початок розробки кошика користувача
    - Форма особистих даних
    - форма доставлення
    - Форма способу оплати

version 0.1.4
- Додано поле фото для Категорії
- Front для сторінки списку товарів
- Додано стандартне фото для товару
- Початок розробки розрахунку через google pay

version 0.1.3
- Перероблена функція додання до бажаного ( реалізовано через js )
    - функція перероблена в модель APIView
    - перенесена в Relation.views

version 0.1.2
- Додано css для Login page
- Оновлено front header

version 0.1.1
- Додано header панель
- Заготовлення для Login page

version 0.1.0
- Готовий функціонал кошика
- Функція на js для реального відображення кількості товарів у кошику
- Початок роботи з Front
- Оновлена робота serial_code_randomizer ( перші 2 цифри - id категорії )
- Фікс тестів ( в основному для cart )
- Видалення serializer для cart ( непотрібен )

version 0.0.15
- Оновлено механізм відповіді на відгук ( додана форма для кожного відгуку )
- Тести для Cart
- Готовий back-end для кошика

version 0.0.14.a
- Додана нова app - cart
- Виправлення ImDeathS
    - Додана нова гілка для Front-end (css|html)
    - Видалено файл HTML
- В розробці кошик для товарів

version 0.0.14
- Поле in_liked перенесене до MainModel
- Додана функція "додати в обране"
- Об'єднанні html сторінки товару в 1 (view_page)
- Додана можливість відновити пароль через пошту

version 0.0.13
- Функція обробки відгуків перенесена в relations/utils ( pre_save )
- Додана можливість відповідати на відгуки ( може відповідати тільки персонал )
- Реалізована функція видалення відгуку для user та для staff
- Дефолтна оцінка в Relation змінена на None, добавленні blank=True, null=True
- В адмінці при створенні товару, категорія створюється автоматично
- Видалений url для зв'язку ( більше не потрібний, бо змінено логіка роботи )
- Оновленні всі шаблони view_.html 
- Оновленні всі products/views
- Relation.parent змінено на on_delete=models.CASCADE

version 0.0.12
- Виправленні тести
- Перенесено url зв'язку з products в relations
- Змінено url для відправлення відгуку
- Змінено рівень доступу в ClothViewSet на AuthenticatedOrReadOnly для перевірки вірності відгуків
- Видалено декоратор підрахунку кількості виклику функції встановлення рейтингу

version 0.0.11
- Об'єднанні моделі коментаріїв та зв'язку
- Робочі відгуки для товарів

version 0.0.10
- Створений новий додаток relations
    - Переміщені всі моделі де є зв'язок між юзером та товаром
- граматичні виправлення в README.md
- Додано профіль юзеру
    - автоматично створюється при реєстрації ( звичайної | google )

version 0.0.9
- Добавлена інформація в html файлах про залогіненого юзера
- Добавлено профіль для User

version 0.0.8
- Добавленні шаблони html сторінок
- Дописані serializer`s для інших категорій
- Модель Rating перейменована в Relation
- Добавлене поле in_liked в модель Relation
- Дописані роутери для інших категорій та об'єктів
- Покращено вигляд об'єктів в admin.py
- Фікс тестів

version 0.0.7.a
- Робочий варіант реєстрації та логіну за допомогою oauth2 та базовими методами авторизації

version 0.0.7
- Розроблена кастомна модель User
- Оновленні тести
- Добавленні djoser та jwt
- Добавленні базові templates
- Доданий додаток users
- Реєстрація та логін користувача  (логін за email | username)
    - Реєстрація через підтвердження через пошту
- Warnings - social_user() missing 1 required positional argument: 'uid'

version 0.0.6
- Добавленні нові поля для виводу в серіалізаторі "одягу"
- Добавлено серіалізатор для рейтингу, а також в admin.py за для запобігання створення дублюючих рейтингів
- Допрацьоване кешуюче поле рейтингу в головній моделі
- Добавленні тести для рейтингу

version 0.0.5
- Допрацьована робота генератора серійного номера
- Нове /кешуючи\ поле rating у mainmodel ( в розробці )
- Виправлені методи save в admin.py для інших моделей
- Додано файл test_utlis 

version 0.0.4
- Добавленні поля discount, viewed для mainmodel
- Добавленні annotaion для оптимізації sql запитів + тести

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
- Додана можливість аутентифікації через Google

version init
- Моделі для одягу, ігрової периферії, товарів для дому
- тести для моделей (створення, фільтр, пошук)
