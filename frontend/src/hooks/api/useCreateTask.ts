import { useMutation, type UseMutationOptions } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { API_ENDPOINTS } from '@/lib/api/endpoints';
import { CreateTaskInput } from '@/lib/validation/schemas';
import { InternalTask } from '@/types';

interface UseCreateTaskOptions {
  bookingId: number | string;
  onSuccess?: (task: InternalTask) => void;
  onError?: (error: Error) => void;
}

export const useCreateTask = ({
  bookingId,
  onSuccess,
  onError,
}: UseCreateTaskOptions): UseMutationOptions<
  InternalTask,
  Error,
  CreateTaskInput,
  unknown
> => {
  return useMutation<InternalTask, Error, CreateTaskInput>({
    mutationKey: ['createTask', bookingId],
    mutationFn: async (data: CreateTaskInput) => {
      const response = await apiClient.post<InternalTask>(
        API_ENDPOINTS.tasks(bookingId),
        data
      );
      return response.data;
    },
    onSuccess,
    onError,
  });
};

export default useCreateTask;
