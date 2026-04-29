import { render, screen, waitFor } from '@testing-library/react';
import BookingPage from '@/app/bookings/[bookingId]/page';
import { useTasks } from '@/hooks/api/useTasks';
import { CreateTaskForm } from '@/components/tasks/CreateTaskForm';
import { TaskList } from '@/components/tasks/TaskList';
import { InternalTask } from '@/types';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the hooks and components
vi.mock('@/hooks/api/useTasks');
vi.mock('@/components/tasks/CreateTaskForm');
vi.mock('@/components/tasks/TaskList');

describe('BookingPage', () => {
  const mockTasks: InternalTask[] = [
    {
      id: 1,
      booking_id: 1,
      title: 'Task 1',
      status: 'OPEN',
      created_at: '2024-01-01T00:00:00Z',
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders booking page with tasks and form', async () => {
    (useTasks as ReturnType<typeof vi.fn>).mockReturnValue({
      data: mockTasks,
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    (CreateTaskForm as ReturnType<typeof vi.fn>).mockReturnValue(
      <div data-testid="create-task-form">Create Task Form</div>
    );

    (TaskList as ReturnType<typeof vi.fn>).mockReturnValue(
      <div data-testid="task-list">Task List</div>
    );

    render(<BookingPage params={{ bookingId: '1' }} />);

    expect(screen.getByText('Booking #1')).toBeInTheDocument();
    expect(screen.getByTestId('create-task-form')).toBeInTheDocument();
    expect(screen.getByTestId('task-list')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    (useTasks as ReturnType<typeof vi.fn>).mockReturnValue({
      data: [],
      isLoading: true,
      error: null,
      refetch: vi.fn(),
    });

    render(<BookingPage params={{ bookingId: '1' }} />);

    // Should show skeletons
    expect(screen.getAllByRole('generic').length).toBeGreaterThan(0);
  });

  it('shows error state', () => {
    const error = new Error('Failed to load');
    (useTasks as ReturnType<typeof vi.fn>).mockReturnValue({
      data: [],
      isLoading: false,
      error,
      refetch: vi.fn(),
    });

    render(<BookingPage params={{ bookingId: '1' }} />);

    expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
    expect(screen.getByText(error.message)).toBeInTheDocument();
  });

  it('shows empty state when no tasks', () => {
    (useTasks as ReturnType<typeof vi.fn>).mockReturnValue({
      data: [],
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    render(<BookingPage params={{ bookingId: '1' }} />);

    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
  });
});
