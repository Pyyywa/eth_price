Описание задачи:
====== 

1. Определить собственные движения цены фьючерса ETHUSDT, исключив из них движения, вызванные влиянием цены BTCUSDT. Описать выбранную методику, подобранные параметры и обоснование в README.
2. Написать программу на Python, которая в реальном времени (с минимальной задержкой) следит за ценой фьючерса ETHUSDT и, используя выбранный метод, определяет собственные движения цены ETH. При изменении цены на 1% за последние 60 минут, программа выводит сообщение в консоль. Программа должна продолжать работать дальше, постоянно считывая актуальную цену.

Структура проекта:
====== 

![image](https://github.com/user-attachments/assets/1c4d1bd1-3945-436e-94ef-81c41c5ff247)


## Установка и запуск


1. Убедитесь, что у вас установлен Python 3.11 и pip.
2. Установите зависимости:

```python
pip install -r requirements.txt
```

Запустите приложение:
```python
python main.py
```

Запуск с использованием Docker
Постройте Docker-образ:
```python
docker build -t price_analysis_app .
```
Запустите контейнер:
```python
docker run --rm -it price_analysis_app
```

Запуск с использованием Docker Compose
Запустите приложение с помощью Docker Compose:
```python
docker-compose up --build
```