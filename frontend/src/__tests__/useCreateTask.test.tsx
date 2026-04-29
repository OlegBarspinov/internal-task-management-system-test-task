import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useCreateTask } from '@/hooks/api/useCreateTask';
import { apiClient } from '@/lib/api/client';
import { CreateTaskInput } from '@/lib/validation/schemas';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// Mock the apiClient
vi.mock('@/lib/api/client', () => ({
  apiClient: {
    post: vi.fn(),
  },
}));

describe('useCreateTask', () => {
  let queryClient: QueryClient;
  const bookingId = 1;
  const mockTask = {
    id: 1,
    booking_id: bookingId,
    title: 'New Task',
    status: 'OPEN' as const,
    created_at: '2024-01-01T00:00:00Z',
  };

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });
    vi.clearAllMocks();
  });

  afterEach(() => {
    queryClient.clear();
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );

  it('should create task successfully', async () => {
    (apiClient.post as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      data: mockTask,
    });

    const { result } = renderHook(
      () => useCreateTask({ bookingId }),
      { wrapper }
    );

    const input: CreateTaskInput = { title: 'New Task' };
    await result.current.mutateAsync(input);

    expect(apiClient.post).toHaveBeenCalledWith(
      `/bookings/${bookingId}/tasks/`,
      input
    );
  });

  it('should handle error', async () => {
    const error = new Error('Failed to create task');
    (apiClient.post as ReturnType<typeof vi.fn>).mockRejectedValueOnce(error);

    const { result } = renderHook(
      () => useCreateTask({ bookingId }),
      { wrapper }
    );

    const input: CreateTaskInput = { title: 'New Task' };
    
    await expect(result.current.mutateAsync(input)).rejects.toThrow(error);
  });
});
