# QA Trainer Pro: Multi-Protocol Testing Landscape

Это профессиональный стенд (Mocking/Simulating Environment), эмулирующий сложную микросервисную архитектуру.
Предназначен для отработки навыков тестирования: gRPC, GraphQL, Kafka, Prometheus, SOAP, REST.

## 🏗 Архитектура

### 1. Сервисы (Docker)
| Сервис | Порт | Описание |
| :--- | :--- | :--- |
| **Core Service** | `8000` (HTTP)<br>`50051` (gRPC) | Главный монолит, запускающий REST, GraphQL, WS и gRPC интерфейсы. |
| **Postgres** | `5432` | Основное хранилище данных. |
| **Kafka** | `9092` | Брокер сообщений. |
| **Prometheus** | `9090` | Сбор метрик с сервиса. |
| **Grafana** | `3000` | Визуализация метрик (Login: admin/admin). |

### 2. Интерфейсы (Protocols)

*   **REST**: `POST /api/users?username=alice` — Создает юзера и отправляет событие в Kafka.
*   **GraphQL**: `POST /graphql` — Получение заказов.
*   **gRPC**: `CalculatePrice` (см. `protos/delivery.proto`) — Расчет доставки.
*   **SOAP**: `POST /soap/currency` — XML эндпоинт.
*   **WS**: `/ws/notifications` — WebSocket поток.

## ⚙️ Настройка окружения
Перед запуском создайте файл конфигурации:
1. Скопируйте пример:
   ```bash
   cp .env.example .env
   ```
2. Отредактируйте `.env` под ваши нужды (пароли, хосты).

Ключевые переменные:
- `POSTGRES_*`: доступы к БД
- `APP_BASE_URL`: адрес приложения
- `ENV`: окружение (local/prod)

## 🛠 Установка

**Внимание**: Проект требует много ресурсов (минимум 4GB RAM для Docker).

1.  **Установка зависимостей и генерация Proto-кода**:
    ```bash
    make install
    ```

2.  **Запуск системы**:
    ```bash
    make up
    ```

3.  **Проверка доступности**:
    *   Swagger UI: `http://localhost:8000/docs`
    *   GraphQL IDE: `http://localhost:8000/graphql`
    *   Prometheus Targets: `http://localhost:9090/targets`

## 👨‍💻 Инженерные задачи (Engineering Challenges)

### Case 1: Kafka Consumer
Написать Python-скрипт (используя `aiokafka`), который подписывается на топик `user_events`.
Затем дернуть ручку `POST /api/users` и проверить, что сообщение пришло.

### Case 2: gRPC Binary Test
Взять файл `protos/delivery.proto`. Сгенерировать клиентский код (команда в `make install` это делает).
Написать тест, который вызывает метод `CalculatePrice(distance=100)` и проверяет цену.

### Case 3: Observability Check
Сделать 20 запросов к API.
Зайти в Prometheus и написать PromQL запрос: `rate(http_requests_total[1m])`. Если график изменился — вы молодец.

### Case 4: GraphQL Fragments
Написать сложный GraphQL запрос, запрашивающий `order(id: 1)` со всеми вложенными `items`, используя фрагменты.
