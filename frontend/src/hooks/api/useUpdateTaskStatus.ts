import { useMutation, type UseMutationOptions } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { API_ENDPOINTS } from '@/lib/api/endpoints';
import { UpdateTaskStatusInput } from '@/lib/validation/schemas';
import { InternalTask } from '@/types';

interface UseUpdateTaskStatusOptions {
  bookingId: number | string;
  taskId: number;
  onSuccess?: (task: InternalTask) => void;
  onError?: (error: Error) => void;
}

export const useUpdateTaskStatus = ({
  bookingId,
  taskId,
  onSuccess,
  onError,
}: UseUpdateTaskStatusOptions): UseMutationOptions<
  InternalTask,
  Error,
  UpdateTaskStatusInput,
  unknown
> => {
  return useMutation<InternalTask, Error, UpdateTaskStatusInput>({
    mutationKey: ['updateTaskStatus', bookingId, taskId],
    mutationFn: async (data: UpdateTaskStatusInput) => {
      const response = await apiClient.patch<InternalTask>(
        API_ENDPOINTS.task(bookingId, taskId),
        data
      );
      return response.data;
    },
    onSuccess,
    onError,
  });
};

export default useUpdateTaskStatus;
