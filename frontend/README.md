# KeyGo Frontend

Frontend часть приложения для управления внутренними задачами (Internal Tasks) на базе Next.js 14 с TypeScript.

## 🚀 Быстрый старт

### 1. Установка Node.js

Требуется Node.js 18+ (рекомендуется 20 LTS). Проверьте версию:

```bash
node --version
npm --version
```

### 2. Установка зависимостей

```bash
cd frontend
npm install
```

**Примечание:** Если `npm install` завершается с ошибкой, попробуйте:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 3. Настройка переменных окружения

Создайте файл `.env.local` на основе `.env.example`:

```bash
# На Windows (PowerShell)
Copy-Item .env.example .env.local

# На macOS/Linux
cp .env.example .env.local
```

Отредактируйте `.env.local` и укажите URL вашего backend API:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_QUERY_DEVTOOLS=true
```

### 4. Запуск development сервера

```bash
npm run dev
```

Приложение будет доступно по адресу [http://localhost:3000](http://localhost:3000).

### 5. Проверка работы

Откройте в браузере: `http://localhost:3000/bookings/1`

Вы должны увидеть страницу задач для бронирования #1.


## 🛠️ Технологический стек

| Категория | Технология |
|-----------|------------|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript |
| State Management | TanStack Query v5 |
| UI Library | shadcn/ui (Radix UI + Tailwind CSS) |
| Forms | React Hook Form + Zod |
| HTTP Client | Axios |
| Testing | Jest + React Testing Library + Vitest |
| Linting | ESLint |
| Formatting | Prettier |

## 🔗 API Endpoints

Приложение взаимодействует с backend по следующим endpoint'ам:

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/v1/bookings/{booking_id}/tasks/` | Получение списка задач |
| POST | `/api/v1/bookings/{booking_id}/tasks/` | Создание новой задачи |
| PATCH | `/api/v1/bookings/{booking_id}/tasks/{task_id}/status` | Обновление статуса задачи |

### Модели данных

```typescript
interface InternalTask {
  id: number;
  booking_id: number;
  title: string;
  status: 'OPEN' | 'IN_PROGRESS' | 'CLOSED';
  created_at: string; // ISO datetime
}

interface CreateTaskRequest {
  title: string; // 1-255 characters
}

interface UpdateTaskStatusRequest {
  status: 'OPEN' | 'IN_PROGRESS' | 'CLOSED';
}
```


## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
npm test

# С покрытием кода
npm run test:coverage

# Watch mode для разработки
npm run test:watch
```

## 🔧 Устранение неполадок

### Ошибка: `'next' is not recognized`

**Причина:** Зависимости не установлены или установлены некорректно.

**Решение:**
```bash
# 1. Очистите кэш npm
npm cache clean --force

# 2. Удалите node_modules и lock-файл
rm -rf node_modules package-lock.json

# 3. Установите зависимости заново
npm install

# 4. Проверьте, что next установлен
npm list next

# 5. Запустите dev сервер
npm run dev
```

### Ошибка: `Cannot find module '...'`

**Причина:** Отсутствуют зависимости или проблемы с импортами.

**Решение:**
```bash
# Переустановите все зависимости
npm install

# Проверьте package.json на наличие всех зависимостей
cat package.json
```

### Проблемы с портом 3000

**Решение:** Используйте другой порт:
```bash
PORT=3001 npm run dev
# или
npx next dev -p 3001
```

### Backend не отвечает

**Проверьте:**
1. Backend сервер запущен на `http://localhost:8000`
2. В `.env.local` указан правильный `NEXT_PUBLIC_API_URL`
3. CORS настроен на backend для `http://localhost:3000`

### Ошибки TypeScript

**Решение:**
```bash
# Проверьте типы
npx tsc --noEmit

# Если есть ошибки, проверьте версии зависимостей
npm outdated
```

### Структура тестов

- **Unit тесты**: Хуки API, утилиты, валидационные схемы
- **Component тесты**: UI компоненты (TaskStatusBadge, TaskList, CreateTaskForm)
- **Integration тесты**: Полные пользовательские сценарии (BookingPage)

### Покрытие

Цель: минимум 80% покрытия критической логики (хуки, валидация, компоненты).

## 🎨 Компоненты

### UI Компоненты (shadcn/ui)

Используются готовые компоненты из `components/ui/`:
- `Button` - Кнопки с вариациями
- `Input` - Поля ввода
- `Label` - Метки форм
- `Select` - Выпадающие списки
- `Card` - Контейнеры
- `Skeleton` - Загрузочные плашки

### Фичевые компоненты

- `TaskList` - Список задач с состояниями (загрузка, ошибка, пусто)
- `TaskItem` - Элемент задачи с управлением статусом
- `TaskStatusBadge` - Бейдж статуса
- `CreateTaskForm` - Форма создания задачи с валидацией

## 🔄 State Management

### React Query (TanStack Query)

Используется для управления серверным состоянием:

- **Кеширование** - Автоматическое кеширование запросов
- **Оптимистичные обновления** - Мгновенный UI отклик
- **Retry** - Автоматические повторы при ошибках
- **Stale Time** - Контроль актуальности данных

### Локальное состояние

- Формы: `react-hook-form`
- UI состояния: `useState`

## ✅ Валидация

### Zod схемы

Расположены в `lib/validation/schemas.ts`:

```typescript
// Создание задачи
createTaskSchema = z.object({
  title: z.string().min(1).max(255).trim(),
});

// Обновление статуса
updateTaskStatusSchema = z.object({
  status: z.enum(['OPEN', 'IN_PROGRESS', 'CLOSED']),
});
```

Интеграция с React Hook Form через `@hookform/resolvers`.

## 🐛 Обработка ошибок

### Централизованная обработка

- **API клиент** (`lib/api/client.ts`) - интерсепторы для всех запросов
- **Логирование** - ошибки логируются в консоль (development)
- **Пользовательские сообщения** - понятные уведомления

### Сценарии ошибок

| Код | Сценарий | Обработка |
|-----|----------|-----------|
| 409 | Дублирование задачи | Показ сообщения "Task already exists" |
| 404 | Бронирование не найдено | Показ ошибки "Invalid Booking ID" |
| 422 | Валидация | Показ полей с ошибками |
| 500 | Серверная ошибка | Общее сообщение "Something went wrong" |

## 🎯 Оптимизации

- **React Query** - кеширование и фоновые обновления
- **Оптимистичные обновления** - мгновенный отклик UI
- **Lazy loading** - по необходимости
- **Memoization** - `useCallback`, `useMemo` для минимизации ре-рендеров

## 🔐 Безопасность

- Валидация на клиенте и сервере
- XSS защита через экранирование (React по умолчанию)
- CSP заголовки (настраиваются в Next.js)

## 📱 Accessibility

- Семантический HTML
- ARIA атрибуты где необходимо
- Клавиатурная навигация
- Достаточная контрастность

## 🚀 Production

### Сборка

```bash
npm run build
npm run start
```


