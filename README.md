# CI/CD со скриптами на Python — демо

Минимальный GitHub Actions pipeline, который последовательно запускает два Python-скрипта. Каждый скрипт обращается к публичному API без токенов и выводит цветные логи в консоль workflow.

## Как это работает

Проект состоит из трёх файлов:

| Файл | Назначение |
|------|------------|
| `.github/workflows/weather&exchange.yml` | CI/CD — оркестратор (GitHub Actions workflow) |
| `.github/scripts/weather.py` | Получение погоды в Москве |
| `.github/scripts/exchange.py` | Получение курсов USDT и TON |

### Схема pipeline

```
[CI/CD] calling weather
    └── weather.py
            [WEATHER]: started
            [WEATHER]: Moscow: +26.5°C, mainly clear
            [WEATHER]: done
[CI/CD] moving to exchange
    └── exchange.py
            [EXCHANGE]: started
            [EXCHANGE]: USDT: $0.9989
            [EXCHANGE]: TON: $1.6800
            [EXCHANGE]: done
[CI/CD] all succeeded ✓
```

Если один из скриптов завершится с ошибкой (сеть, некорректный ответ API), workflow останавливается и выводит красное сообщение `[CI/CD ERROR]` с кодом выхода.

### Внешние API

Оба API бесплатные и не требуют ключей:

- **Погода** — [Open-Meteo](https://open-meteo.com/) (`api.open-meteo.com`)
- **Курсы криптовалют** — [CoinGecko](https://www.coingecko.com/) public API (`api.coingecko.com`)

### Цвета логов

| Префикс | Цвет |
|---------|------|
| `[CI/CD]` | Белый |
| `[WEATHER]`, `[EXCHANGE]` | Синий |
| `[CI/CD]: all succeeded` | Зелёный |
| `[CI/CD ERROR]`, `[WEATHER ERROR]`, `[EXCHANGE ERROR]` | Красный (жирный) |

## Запуск

### На GitHub

1. Запушьте репозиторий на GitHub.
2. Откройте **Actions → Weather & Exchange**.
3. Запустите вручную через **Run workflow** или сделайте push в ветку `main` / `master`.

### Локально

Повторите те же шаги, что выполняет workflow:

```bash
echo -e "\033[97m[CI/CD]: calling weather\033[0m"
python3 .github/scripts/weather.py

echo -e "\033[97m[CI/CD]: moving to exchange\033[0m"
python3 .github/scripts/exchange.py

echo -e "\033[92m\033[1m[CI/CD]: all succeeded ✓\033[0m"
```

Внешние зависимости не нужны — скрипты используют только стандартную библиотеку Python.

## Структура проекта

```
.
├── .github/
│   ├── workflows/
│   │   └── weather&exchange.yml   # GitHub Actions workflow
│   └── scripts/
│       ├── weather.py             # Скрипт погоды
│       └── exchange.py            # Скрипт курсов
├── .gitignore
└── README.md
```
