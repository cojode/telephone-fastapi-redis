# Задание первое (практическое)

## Запуск

1) Создать `.env` из `.example.env`: 
```sh
cp .env.example .env
```

2) Запустить, развернув сервис на 8000 порте согласно `docker-compose.yml`:
```sh
docker compose up --build -d
```

3) Проверить доступность документации по эндпоинту: `localhost:8000/api/docs`

## Эндпоинты:

* `GET /api/address/{phone}` - достать телефон-адрес

* `PUT /api/address/{phone}` - обновить адрес по телефону

* `DELTE /api/address/{phone}` - удалить запись телефон-адрес

* `GET /api/address/{phone}` - создать запись телефон-адрес

Подробнее в swagger-документации: `localhost:8000/api/docs`
