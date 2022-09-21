# Алексей Губер - "Подвези соседа!"
# Пользовательские сценарии


### Группа: 10И2
### Электронная почта: aoguber@edu.hse.ru
### VK: www.vk.com/hoisala

<br/>

### Сценарий 1. Вход и регистрация:
1. Форма для ввода логина и пароля, если пользователь уже зарегистирован.
2. После успешной авторизации, пользователь переходит в личный кабинет
3. Если у пользователя не было аккаунта ранее, он его создает в форме для регистрации.
4. После ввода данных, соответсвующих формату, пользователю приходит на почту ссылка для подтверждения 
5. Присутсвует возможность изменить адрес электронной почты, если при регистрации вы ошиблись.
6. После перехода по ссылке в письме, отображается сообщение об успешном подтверждении адреса электронной поты.
7. Сам пользовать переходит в личный кабинет.
8. Настройки (заслуживает отдельного сценария):
    1. Пользователю доступен просмотр и изменения информации о профиле и настройки поведения приложения
    2. Можно изменить аватарку, имя, фамилию, телефон, почту (после изменения адреса почты, профиль имеет статус неподтвержденного, а на указанный адрес вновь приходит ссылка для подтверждения)
    3. После перехода по ссылке подтверждения адреса электронной почты в письме, отображается сообщение об успешном подтверждении адреса электронной поты.
    4. Можно изменить пароль
    5. Можно указать описание профиля, а также домашний адрес пользователя, чтобы иметь возможность принимать участие в поездках.
    6. Указать радиус поиска поездок
    7. Пользователь может перейти на другие страницы сайта благодаря меню.

### Сценарий 2. Личный кабинет:
1. Пользователь имеет возможность посмотреть информацию в своем профиле, которую он указывал при регистрации.
2. Пользователь имеет возможность посмотреть информацию в своем профиле, которую он указал в настройках (например, загрузил аватар).
3. Пользователь может добавить описание к своему профилю.
4. Пользователь должен добавить свой домашний адрес в профиль, чтобы иметь возможность принимать участие в поездках
5. При нажатии на кнопку выхода из аккаунта, перед пользователем появляется страница логина.
6. Если нажать на иконку человека с рукой и чемоданом в меню, то пользователь перейдет на страницу пассажира.
7. Если нажать на иконку машины в меню, то пользователь перейдет на страницу водителя.
8. Если нажать на шестеренку в меню, можно перейти в настройки

### Сценарий 3. Админ-панель:
1. Только администратор сайта имеет возможность войти в панель администратора. (Список администраторов указывается в конфигурационном файле)
2. Администратор имеет возможность выйти из админ-панели и перейти в обычный личный кабинет, где он может выполнять все те же действия, что и обычный пользователь.
3. Администратор может в удобном виде просматривать любую информацию из всех таблиц базы данных.
4. Администратор может сортировать вывод информации из базы данных по опреденному столбцу.
5. Администратор может изменять отдельно выбранную строку в таблице базы данных.
6. Администратор может выделить несколько строк для осуществления одинаковых действий с ними.
7. Администратор может удалять выбранные строки из таблиц базы данных.

### Сценарий 4. Роль водителя:
1. Просмотр информации о всех будущих поездках, а также подробно о конкретно выбранной поездке, с возможностью отредактировать описание. Информация включает в себя в том числе и ссылки на профили ваших пассажиров.
2. Просмотр истории своих поездок в качестве водителя. Информация включает в себя в том числе и ссылки на профили ваших пассажиров.
3. Переход на страницу создания новой поездки. Если пользователь не указал в профиле свой домашний адрес, создать новую поездку не выйдет. Вместо этого появится уведомление о необходимости указать свой домашний адрес.
4. Пользователь может перейти на другие страницы сайта благодаря меню.
5. Если нажать на иконку человека с рукой и чемоданом в меню, то пользователь перейдет на страницу пассажира.
6. Если нажать на иконку человека в меню, то можно перейти в свой профиль
7. Если нажать на шестеренку в меню, можно перейти в настройки

### Сценарий 5. Создание поездки:
1. Выбор типа поездки (В город или домой)
2. В соответвии с выбором типа, указываем или адрес места, куда мы едем в город, или адрес места, откуда мы едем домой.
3. Для удобства пользователя, при вводе адреса внизу появляются подсказки. 
4. Если среди подсказок нет нужного адреса, у пользователя есть возможность указать точку на карте.
5. Выбор дня поездки
6. Выбор времени поездки
7. Выбор максимального числа пассажиров, которых вы готовы подвезти
8. Описание поездки (например, номер подъезда, у которого вы заберете пассажиров)
9. Если все поля заполнены (описание по желанию), то после нажатия соответсвующей кнопки, поездка появится у пассажиров поблизости.
10. Если вы успешно все заполнили, но найдена уже существующая поездка, с похожими характеристиками на вашу, у вас есть возможность присоединиться в качестве пассажира.
11. Если нажать на иконку человека с рукой и чемоданом в меню, то пользователь перейдет на страницу пассажира.
12. Если нажать на иконку человека в меню, то можно перейти в свой профиль
13. Если нажать на шестеренку в меню, можно перейти в настройки

### Сценарий 6. Указание адреса на карте:
1. Можно вернуться на предыдущую страницу
2. Можно найти нужный адрес, введя его в форму для поиска адреса (может быть полезно, например, если вы помните адрес близлежащей улицы, но нужно указать конкретную точку)
3. Можно масштабироваться и перемещать карту на экране
4. При выборе точки на карте (клике), отображается краткая информация о месте (адрес)
5. При выборе точки на карте, есть возможность отменить выбор
6. При выборе точки на карте рядом с адресом отобрается кнопка "Выбрать этот адрес"
7. При нажатии на кнопку "Выбрать этот адрес", пользователь переходит обратно на страницу создания поездки, где поле для выбора адреса уже заполненно.

### Сценарий 7. Роль пассажира:
1. Если существуют поездки в город или обратно, указанный адрес которых близок от указанного в вашем профиле, то такие поездки появятся у вас в списке с возможностью присоединиться в качестве пассажира.
2. Если вы присоединились к какой-то поездке, то будет показано уведомление, а вы будете добавлены в список пассажиров.
3. Вверху списка будут показаны поездки, к которым вы присоединились в качестве пассажира.
4. Доступные поездки отображаются не все сразу, на странице присутсвует кнопка "Показать еще", чтобы страница сайта открывалась быстрее.
5. Если нажать на иконку машины в меню, то пользователь перейдет на страницу водителя.
6. Если нажать на иконку человека в меню, то можно перейти в свой профиль
7. Если нажать на шестеренку в меню, можно перейти в настройки