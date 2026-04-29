import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CreateTaskForm } from '@/components/tasks/CreateTaskForm';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useCreateTask } from '@/hooks/api/useCreateTask';

// Mock the useCreateTask hook
vi.mock('@/hooks/api/useCreateTask', () => ({
  useCreateTask: vi.fn(),
}));

describe('CreateTaskForm', () => {
  const mockOnSuccess = vi.fn();
  const bookingId = 1;

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders form correctly', () => {
    render(<CreateTaskForm bookingId={bookingId} onSuccess={mockOnSuccess} />);
    
    expect(screen.getByLabelText(/task title/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create task/i })).toBeInTheDocument();
  });

  it('shows validation error for empty title', async () => {
    const user = userEvent.setup();
    render(<CreateTaskForm bookingId={bookingId} onSuccess={mockOnSuccess} />);
    
    const submitButton = screen.getByRole('button', { name: /create task/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });
  });

  it('shows validation error for title longer than 255 characters', async () => {
    const user = userEvent.setup();
    render(<CreateTaskForm bookingId={bookingId} onSuccess={mockOnSuccess} />);
    
    const input = screen.getByLabelText(/task title/i);
    const longTitle = 'a'.repeat(256);
    await user.type(input, longTitle);
    
    const submitButton = screen.getByRole('button', { name: /create task/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/title must be less than 255 characters/i)).toBeInTheDocument();
    });
  });

  it('submits form successfully', async () => {
    const user = userEvent.setup();
    const mockMutateAsync = vi.fn().mockResolvedValue({
      id: 1,
      booking_id: bookingId,
      title: 'New Task',
      status: 'OPEN',
      created_at: new Date().toISOString(),
    });
    
    (useCreateTask as ReturnType<typeof vi.fn>).mockReturnValue({
      mutateAsync: mockMutateAsync,
      isPending: false,
    });
    
    render(<CreateTaskForm bookingId={bookingId} onSuccess={mockOnSuccess} />);
    
    const input = screen.getByLabelText(/task title/i);
    await user.type(input, 'New Task');
    
    const submitButton = screen.getByRole('button', { name: /create task/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockMutateAsync).toHaveBeenCalledWith({ title: 'New Task' });
    });
  });

  it('handles 409 conflict error', async () => {
    const user = userEvent.setup();
    const error = {
      response: { status: 409 },
      message: 'Duplicate task',
    };
    
    const mockMutateAsync = vi.fn().mockRejectedValue(error);
    
    (useCreateTask as ReturnType<typeof vi.fn>).mockReturnValue({
      mutateAsync: mockMutateAsync,
      isPending: false,
    });
    
    render(<CreateTaskForm bookingId={bookingId} onSuccess={mockOnSuccess} />);
    
    const input = screen.getByLabelText(/task title/i);
    await user.type(input, 'Duplicate Task');
    
    const submitButton = screen.getByRole('button', { name: /create task/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/task with this title already exists/i)).toBeInTheDocument();
    });
  });
});
