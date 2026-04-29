import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useUpdateTaskStatus } from '@/hooks/api/useUpdateTaskStatus';
import { apiClient } from '@/lib/api/client';
import { UpdateTaskStatusInput } from '@/lib/validation/schemas';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// Mock the apiClient
vi.mock('@/lib/api/client', () => ({
  apiClient: {
    patch: vi.fn(),
  },
}));

describe('useUpdateTaskStatus', () => {
  let queryClient: QueryClient;
  const bookingId = 1;
  const taskId = 1;
  const mockUpdatedTask = {
    id: taskId,
    booking_id: bookingId,
    title: 'Updated Task',
    status: 'IN_PROGRESS' as const,
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

  it('should update task status successfully', async () => {
    (apiClient.patch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      data: mockUpdatedTask,
    });

    const { result } = renderHook(
      () => useUpdateTaskStatus({ bookingId, taskId }),
      { wrapper }
    );

    const input: UpdateTaskStatusInput = { status: 'IN_PROGRESS' };
    const resultData = await result.current.mutateAsync(input);

    expect(apiClient.patch).toHaveBeenCalledWith(
      `/bookings/${bookingId}/tasks/${taskId}/status`,
      input
    );
    expect(resultData).toEqual(mockUpdatedTask);
  });

  it('should handle error', async () => {
    const error = new Error('Failed to update status');
    (apiClient.patch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(error);

    const { result } = renderHook(
      () => useUpdateTaskStatus({ bookingId, taskId }),
      { wrapper }
    );

    const input: UpdateTaskStatusInput = { status: 'CLOSED' };
    
    await expect(result.current.mutateAsync(input)).rejects.toThrow(error);
  });
});
