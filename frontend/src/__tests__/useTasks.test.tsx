import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useTasks } from '@/hooks/api/useTasks';
import { apiClient } from '@/lib/api/client';
import { InternalTask } from '@/types';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// Mock the apiClient
vi.mock('@/lib/api/client', () => ({
  apiClient: {
    get: vi.fn(),
  },
}));

const mockTasks: InternalTask[] = [
  {
    id: 1,
    booking_id: 1,
    title: 'Test Task 1',
    status: 'OPEN',
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    booking_id: 1,
    title: 'Test Task 2',
    status: 'IN_PROGRESS',
    created_at: '2024-01-02T00:00:00Z',
  },
];

describe('useTasks', () => {
  let queryClient: QueryClient;
  const bookingId = 1;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
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

  it('should fetch tasks successfully', async () => {
    (apiClient.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      data: mockTasks,
    });

    const { result } = renderHook(() => useTasks({ bookingId }), { wrapper });

    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.data).toEqual(mockTasks);
  });

  it('should handle error', async () => {
    const error = new Error('API Error');
    (apiClient.get as ReturnType<typeof vi.fn>).mockRejectedValueOnce(error);

    const { result } = renderHook(() => useTasks({ bookingId }), { wrapper });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });

  it('should not fetch when bookingId is falsy', async () => {
    (apiClient.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      data: mockTasks,
    });

    renderHook(() => useTasks({ bookingId: null as unknown as number }), {
      wrapper,
    });

    // The query should not be enabled
    await waitFor(() => {
      expect(apiClient.get).not.toHaveBeenCalled();
    });
  });
});
