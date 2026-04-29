# Frontend Implementation Plan - KeyGo Internal Tasks

## Overview

Реализация фронтенд части для сервиса управления внутренними задачами (Internal Tasks) на базе Next.js + React с использованием чистой архитектуры и лучших практик для продакшн кода.

## Technical Requirements

- **Framework**: Next.js 13+ (App Router)
- **Language**: TypeScript
- **State Management**: React Query (TanStack Query) для серверного состояния
- **UI Library**: shadcn/ui (на базе Radix UI и Tailwind CSS)
- **Form Handling**: React Hook Form с Zod валидацией
- **API Communication**: Axios или Fetch API с кастомным хуком
- **Testing**: Jest + React Testing Library
- **Architecture**: Чистая архитектура с разделением на слои

## API Endpoints Analysis

На основе изучения `backend/src/app/api/tasks.py`:

### Base URL Pattern
```
/api/v1/bookings/{booking_id}/tasks
```

### Available Endpoints
1. **POST** `/api/v1/bookings/{booking_id}/tasks/` - Создание задачи
   - Request: `{ "title": "string" }`
   - Response: `InternalTask` объект
   - Errors: 409 (duplicate), 422 (validation), 500 (server)

2. **GET** `/api/v1/bookings/{booking_id}/tasks/` - Получение списка задач
   - Response: `InternalTask[]` массив
   - Errors: 500 (server)

3. **PATCH** `/api/v1/bookings/{booking_id}/tasks/{task_id}/status` - Обновление статуса
   - Request: `{ "status": "OPEN|IN_PROGRESS|CLOSED" }`
   - Response: Обновленный `InternalTask` объект
   - Errors: 404 (not found), 400 (invalid status), 422 (validation), 500 (server)

### Data Models (из schemas.py и models.py)
```typescript
interface InternalTask {
  id: number;
  booking_id: number;
  title: string;
  status: 'OPEN' | 'IN_PROGRESS' | 'CLOSED';
  created_at: string; // ISO datetime
}

interface CreateTaskRequest {
  title: string; // minLength: 1, maxLength: 255
}

interface UpdateTaskStatusRequest {
  status: 'OPEN' | 'IN_PROGRESS' | 'CLOSED';
}
```

## Clean Architecture Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── bookings/
│   │   └── [bookingId]/
│   │       ├── page.tsx    # Основная страница
│   │       ├── layout.tsx  # Layout для страницы
│   │       └── tasks/      # Вложенные маршруты для задач (если понадобится)
│   ├── api/                # API маршруты (если нужны прокси)
│   └── layout.tsx          # Корневой layout
├── components/             # Переиспользуемые UI компоненты
│   ├── ui/                 # shadcn/ui компоненты
│   ├── tasks/              # Компоненты специфичные для задач
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── CreateTaskForm.tsx
│   │   └── TaskStatusBadge.tsx
│   └── layout/             # Layout компоненты
├── hooks/                  # Кастомные React хуки
│   ├── api/                # Хуки для работы с API
│   │   ├── useTasks.ts
│   │   └── useCreateTask.ts
│   └── ui/                 # UI хуки
├── lib/                    # Утилиты и вспомогательные функции
│   ├── api/                # API клиенты и конфигурация
│   │   ├── client.ts
│   │   └── endpoints.ts
│   ├── utils/              # Общие утилиты
│   └── validation/         # Схемы валидации
├── types/                  # TypeScript типы и интерфейсы
│   ├── api/                # API связанные типы
│   │   ├── tasks.ts
│   │   └── index.ts
│   └── index.ts
├── store/                  # Состояние приложения (если понадобится помимо React Query)
│   └── index.ts
├── styles/                 # Стили и темы
│   └── globals.css
├── tests/                  # Тесты
│   ├── components/
│   ├── hooks/
│   └── utils/
├── constants/              # Константы
└── utils/                  # Вспомогательные функции
```

## Implementation Steps

### 1. Project Setup
- [ ] Инициализация Next.js проекта с TypeScript
- [ ] Настройка ESLint и Prettier
- [ ] Настройка Tailwind CSS и shadcn/ui
- [ ] Настройка React Query
- [ ] Настройка Axios/Fetch API клиента
- [ ] Настройка Jest и React Testing Library

### 2. Core Infrastructure
- [ ] Создание API клиента с обработкой ошибок и интерсепторами
- [ ] Определение TypeScript типов для API ответов и запросов
- [ ] Создание констант для API endpoints
- [ ] Настройка React Query провайдера

### 3. Features Implementation

#### 3.1 Tasks Listing
- [ ] Создание хука `useTasks` для получения списка задач
- [ ] Реализация компонента `TaskList` с загрузкой и обработкой ошибок
- [ ] Реализация компонента `TaskItem` для отображения отдельной задачи
- [ ] Реализация компонента `TaskStatusBadge` для визуализации статуса

#### 3.2 Task Creation
- [ ] Создание хука `useCreateTask` для создания задач
- [ ] Реализация формы создания задачи с валидацией (React Hook Form + Zod)
- [ ] Обработка успешного создания и ошибок (включая 409 Conflict)
- [ ] Оптимистичное обновление UI

#### 3.3 Status Updates
- [ ] Создание хука `useUpdateTaskStatus` для изменения статуса
- [ ] Интеграция с компонентом задачи для обновления статуса
- [ ] Обработка ошибок и состояний загрузки

### 4. Page Implementation
- [ ] Создание страницы `/bookings/[bookingId]` с layout
- [ ] Интеграция всех компонентов на страницу
- [ ] Добавление заголовка и навигации
- [ ] Реализация обработки отсутствующих данных и состояний загрузки

### 5. Error Handling and Loading States
- [ ] Единая обработка ошибок API
- [ ] Состояния загрузки для всех операций
- [ ] Пустые состояния для списка задач
- [ ] Обработка 404 для несуществующих бронирований

### 6. Testing
- [ ] Unit тесты для хуков API
- [ ] Component тесты для UI компонентов
- [ ] Интеграционные тесты для основных пользовательских сценариев
- [ ] Тестирование обработки ошибки дублирования задач

### 7. Documentation and Deployment Preparation
- [ ] Обновление README с инструкциями по запуску frontend
- [ ] Добавление информации о тестировании
- [ ] Подготовка переменных окружения для конфигурации API URL

## Best Practices Implementation

### Code Quality
- Strict TypeScript режим
- ESLint с рекомендуемыми правилами для React/Next.js
- Prettier для форматирования кода
- Компонентный подход с Single Responsibility Principle
- Чистые функции и чистые компоненты где возможно

### Performance
- React Query для кеширования и фоновых обновлений
- Оптимистичные обновления UI
- Ленивая загрузка компонентов где уместно
- Минимизация ре-рендеров через useCallback/useMemo

### Accessibility
- Семантический HTML
- ARIA атрибуты где необходимо
- Достаточная цветовая контрастность
- Фокус管理 для интерактивных элементов

### Error Handling
- Централизованная обработка ошибок API
- Пользовательские сообщения об ошибках
- Graceful degradation при сетевых проблемах
- Логирование ошибок в консоль разработки

### Security
- Защита от XSS через правильное экранирование
- Валидация входных данных на клиенте и сервере
- Безопасное handling пользовательского ввода
- CSP заголовки (на уровне Next.js конфигурации)

## Environment Configuration

### Development
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Production
```
NEXT_PUBLIC_API_URL=https://your-production-domain.com/api/v1
```

## Testing Strategy

### Unit Tests
- Хуки API с мокованными запросами
- Утилиты и функции преобразования данных
- Валидационные схемы

### Component Tests
- Отображение компонентов в различных состояниях
- Обработка пользовательских взаимодействий
- Условный рендеринг на основе пропсов

### Integration Tests
- Полный флоу создания задачи
- Флоу обновления статуса задачи
- Обработка ошибок дублирования
- Состояния загрузки и пустые состояния

## Deployment Considerations

### Build Optimization
- Next.js автоматическое code splitting
- Оптимизация изображений (если понадобится)
- Предварительный рендеринг где уместно
- Анализ бандла для удаленияunused кода

### Monitoring and Logging
- Логирование ошибок в режиме разработки
- Подготовка к интеграции с Sentry (описание в README)
- Метрики производительности (описание в README)

## Risks and Mitigations

### Risk: API Changes
- Mitigation: Абстракция API клиента, легко обновляемый

### Risk: Type Safety Gaps
- Mitigation: Полное TypeScript покрытие, генерация типов из OpenAPI спецификации (если появится)

### Risk: Performance Issues with Large Task Lists
- Mitigation: Пагинация или виртуальная скроллинг (по необходимости)
- Mitigation: Кеширование через React Query

### Risk: Complex State Management
- Mitigation: Использование React Query для серверного состояния
- Mitigation: Локальное состояние только для UI взаимодействий

## Estimated Timeline

### Week 1: Setup and Core Infrastructure
- Project setup and configuration: 2 days
- API client and types: 2 days
- React Query provider and basic hooks: 1 day

### Week 2: Feature Implementation
- Task listing and UI components: 2 days
- Task creation form: 2 days
- Status update functionality: 1 day

### Week 3: Integration and Testing
- Page integration and layout: 1 day
- Error handling and loading states: 1 day
- Unit and component testing: 2 days
- Integration testing: 1 day

### Week 4: Polish and Documentation
- Performance optimization: 1 day
- Accessibility improvements: 1 day
- Documentation and README updates: 1 day
- Final review and QA: 1 day

**Total Estimated Time: 3-4 weeks (adjustable based on experience and requirements)**

## Success Criteria

1. [ ] Страница `/bookings/[bookingId]` отображает список задач для данного бронирования
2. [ ] Пользователь может создать новую задачу с валидацией
3. [ ] Пользователь может изменить статус задачи (OPEN/IN_PROGRESS/CLOSED)
4. [ ] Предотвращено создание дублирующих задач (обработка 409 ошибки)
5. [ ] Все состояния загрузки и ошибок обрабатываются корректно
6. [ ] Единообразный UI с использованием shadcn/ui компонентов
7. [ ] Полная типизация TypeScript во всем приложении
8. [ ] Unit тесты покрывают минимум 80% критической логики
9. [ ] Приложение соответствует лучшим практикам Next.js и React
10. [ ] Чистый, поддерживаемый код с четким разделением ответственности

## Next Steps

После утверждения этого плана:
1. Создать репозиторий для frontend части
2. Инициализировать проект согласно плану
3. Начать с настройки инфраструктуры и API клиента
4. Последовательно реализовать каждую функцию согласно приоритетам