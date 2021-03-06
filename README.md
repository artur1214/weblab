Проект web сервера для хранения препаратов.

## Запуск сервера
Для запуска и настройки понадобится:

> - python 3.8+
> - Соединение с интернетом
> - немножко прямых рук

Для начала скачайте проект

```shell
git clone https://github.com/artur1214/weblab weblab
cd weblab
```
Теперь нам понадобится установить зависимости, вы можете использовать виртуальную среду python
однако на практике, либо вы это понимаете и без меня, либо только что скачали python, чтобы запустить конкретно данный
проект, так что вы и без неё обойдетесь.

Для установки зависимостей нам понадобиться всего лишь запустить одну команду из корня проекта:

```shell
pip install -r weblab/requirements/dev.txt
```
Отлично! Если вы смогли дойти до данного этапа, значит ваш IQ уже стремится бесконечности. (как минимум больше 50)

Теперь нужно сделать кое-что ешё: выполнить миграции, чтобы подготовить базу данных к работе, для этого прсто нужно запустить 
следующую команду:
```shell
python manage.py migrate
```

Остается лишь понять, как запустить проект. Делается это очень легко: всего одна команда, которую нужно запустить из корня проекта:
```shell
python manage.py runserver
```
Поздравляю! Сервер доступен по адресу `127.0.0.1:8000`