import { useQuery, type UseQueryOptions } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { API_ENDPOINTS } from '@/lib/api/endpoints';
import { InternalTask } from '@/types';

interface UseTasksOptions {
  bookingId: number | string;
  enabled?: boolean;
}

export const useTasks = ({
  bookingId,
  enabled = true,
}: UseTasksOptions): UseQueryOptions<InternalTask[], Error> => {
  return useQuery<InternalTask[], Error>({
    queryKey: ['tasks', bookingId],
    queryFn: async () => {
      const response = await apiClient.get<InternalTask[]>(
        API_ENDPOINTS.tasks(bookingId)
      );
      return response.data;
    },
    enabled: enabled && !!bookingId,
    staleTime: 30 * 1000, // 30 seconds
    retry: 2,
  });
};

export default useTasks;
