# Frontend Implementation Task

## Task Description
Реализовать фронтенд часть для сервиса управления внутренними задачами (Internal Tasks) на базе Next.js + React с использованием чистой архитектуры и лучших практик для продакшн кода.

## Requirements
- Страница: `/bookings/[booking_id]`
- Блок Internal Tasks со списком задач, формой создания и сменой статуса
- Использовать: Next.js 13+ (App Router), TypeScript, React Query, shadcn/ui
- Следовать чистой архитектуре и лучшим практикам
- Покрыть unit и интеграционными тестами основные сценарии

## Acceptance Criteria
1. Страница `/bookings/[bookingId]` отображает список задач для данного бронирования
2. Пользователь может создать новую задачу с валидацией
3. Пользователь может изменить статус задачи (OPEN/IN_PROGRESS/CLOSED)
4. Предотвращено создание дублирующих задач (обработка 409 ошибки)
5. Все состояния загрузки и ошибок обрабатываются корректно
6. Единообразный UI с использованием shadcn/ui компонентов
7. Полная типизация TypeScript во всем приложении
8. Unit тесты покрывают минимум 80% критической логики

## Related Documents
- Техническое задание: `ТЗ.md`
- Backend API спецификация: `backend/src/app/api/tasks.py`
- Backend API схемы: `backend/src/app/api/schemas.py`
- Frontend implementation plan: `docs/tasks/frontend-implementation/implementation_plan.md`

## Estimated Effort
3-4 часа согласно ТЗ, но для качественной реализации с тестами и лучшими практиками потребуется больше времени (оценка: 3-4 недели полной занятости).

## Dependencies
- Backend API должен быть запущен и доступен
- Node.js 18+ и npm/yarn/pnpm