import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskItem } from '@/components/tasks/TaskItem';
import { InternalTask } from '@/types';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useUpdateTaskStatus } from '@/hooks/api/useUpdateTaskStatus';

// Mock the useUpdateTaskStatus hook
vi.mock('@/hooks/api/useUpdateTaskStatus', () => ({
  useUpdateTaskStatus: vi.fn(),
}));

describe('TaskItem', () => {
  const mockTask: InternalTask = {
    id: 1,
    booking_id: 1,
    title: 'Test Task',
    status: 'OPEN',
    created_at: '2024-01-01T00:00:00Z',
  };

  const bookingId = 1;

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders task information correctly', () => {
    const mockMutate = vi.fn();
    (useUpdateTaskStatus as ReturnType<typeof vi.fn>).mockReturnValue({
      mutateAsync: mockMutate,
      isPending: false,
    });

    render(<TaskItem task={mockTask} bookingId={bookingId} />);
    
    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Open')).toBeInTheDocument();
  });

  it('allows status change', async () => {
    const user = userEvent.setup();
    const mockMutate = vi.fn().mockResolvedValue({
      ...mockTask,
      status: 'IN_PROGRESS',
    });
    
    (useUpdateTaskStatus as ReturnType<typeof vi.fn>).mockReturnValue({
      mutateAsync: mockMutate,
      isPending: false,
    });

    render(<TaskItem task={mockTask} bookingId={bookingId} />);
    
    const select = screen.getByRole('combobox');
    await user.selectOptions(select, 'IN_PROGRESS');
    
    await waitFor(() => {
      expect(mockMutate).toHaveBeenCalledWith({ status: 'IN_PROGRESS' });
    });
  });

  it('shows loading state during update', async () => {
    const user = userEvent.setup();
    const mockMutate = vi.fn().mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 100))
    );
    
    (useUpdateTaskStatus as ReturnType<typeof vi.fn>).mockReturnValue({
      mutateAsync: mockMutate,
      isPending: true,
    });

    render(<TaskItem task={mockTask} bookingId={bookingId} />);
    
    const select = screen.getByRole('combobox');
    await user.selectOptions(select, 'CLOSED');
    
    // Should show loading spinner
    await waitFor(() => {
      expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
    });
  });
});
