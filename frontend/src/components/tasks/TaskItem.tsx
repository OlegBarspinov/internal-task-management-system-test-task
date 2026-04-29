'use client';

import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useUpdateTaskStatus } from '@/hooks/api/useUpdateTaskStatus';
import { TaskStatusBadge } from './TaskStatusBadge';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Loader2 } from 'lucide-react';
import { InternalTask, TaskStatus } from '@/types';
import { formatDate } from '@/lib/utils';

interface TaskItemProps {
  task: InternalTask;
  bookingId: number | string;
}

const statusOptions: TaskStatus[] = ['OPEN', 'IN_PROGRESS', 'CLOSED'];

export function TaskItem({ task, bookingId }: TaskItemProps) {
  const [isUpdating, setIsUpdating] = useState(false);
  const queryClient = useQueryClient();

  const updateStatusMutation = useUpdateTaskStatus({
    bookingId,
    taskId: task.id,
    onSuccess: (updatedTask) => {
      setIsUpdating(false);
      // Update the task in the query cache optimistically
      queryClient.setQueryData<InternalTask[]>(['tasks', bookingId], (oldTasks = []) => {
        return oldTasks.map((t) => t.id === task.id ? updatedTask : t);
      });
    },
    onError: () => {
      setIsUpdating(false);
    },
  });

  const handleStatusChange = async (newStatus: string) => {
    setIsUpdating(true);
    try {
      await updateStatusMutation.mutateAsync({ status: newStatus as TaskStatus });
    } catch (error) {
      // Error is handled in onError
    }
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
      <div className="flex-1 min-w-0">
        <h3 className="text-sm font-medium text-gray-900 truncate">
          {task.title}
        </h3>
        <p className="text-xs text-gray-500 mt-1">
          Created: {formatDate(task.created_at)}
        </p>
      </div>

      <div className="flex items-center gap-3 ml-4">
        <TaskStatusBadge status={task.status} />

        {isUpdating ? (
          <Loader2 className="h-4 w-4 animate-spin text-gray-500" />
        ) : (
          <Select
            value={task.status}
            onValueChange={handleStatusChange}
            disabled={updateStatusMutation.isPending}
          >
            <SelectTrigger className="w-[140px] h-8 text-xs">
              <SelectValue placeholder="Change status" />
            </SelectTrigger>
            <SelectContent>
              {statusOptions.map((status) => (
                <SelectItem key={status} value={status}>
                  {status.replace('_', ' ')}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}
      </div>
    </div>
  );
}

export default TaskItem;