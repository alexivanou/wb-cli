# Wildberries CLI

CLI утилита для взаимодействия с API маркетплейса Wildberries.

## Возможности

- Получение информации о продавце (`get-seller-info`)
- Управление складами (`get-warehouses`)
- Работа с остатками (`get-inventory`)
- Управление товарами (`get-products`)
- Работа с ценами (`set-price`)
- Работа с медиа (`get-media`)
- И многое другое...

## Установка

## Через PyPI (рекомендуется)

```bash
pip install wb-cli
```

## Из GitHub

```bash
pip install git+https://github.com/alexivanou/wb-cli.git
```

## Локальная установка

```bash
pip install -e .
```

## Использование

### Получение информации о продавце

```bash
wb-cli get-seller-info --token "YOUR_TOKEN"
```

### Получение складов

```bash
wb-cli get-warehouses --token "YOUR_TOKEN"
```

### Получение товаров

```bash
wb-cli get-products --token "YOUR_TOKEN" --limit 10
```

### Проверка соединения

```bash
wb-cli ping --token "YOUR_TOKEN"
```

## Доступные команды

Полный список команд доступен через:

```bash
wb-cli --help
```

## Конфигурация

Вы можете использовать переменные окружения для токенов:

- `WB_TOKEN_GENERAL` — токен для общих операций
- `WB_TOKEN_WAREHOUSE` — токен для работы со складами
- `WB_TOKEN_PRODUCTS` — токен для работы с товарами
- `WB_TOKEN_INVENTORY` — токен для работы с остатками

Пример `.env` файла:

```env
WB_TOKEN_GENERAL=your_token_here
WB_TOKEN_WAREHOUSE=your_warehouse_token
WB_TOKEN_PRODUCTS=your_products_token
```

## Опции команд

Все команды поддерживают опции:

- `--token` — указать токен напрямую
- `--json` — вывод в формате JSON
- `--verbose` (-v) — подробный вывод для отладки

## Требования

- Python 3.12+
- wildberries-python-sdk
- typer
- rich
- pydantic

## Тестирование

```bash
pytest tests/
```

## Лицензия

MIT License

## Авторы

Aliaksandr Ivanou <alexivanou@gmail.com>
