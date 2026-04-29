'use client';

import { Skeleton } from '@/components/ui/skeleton';
import { TaskItem } from './TaskItem';
import { InternalTask } from '@/types';
import { AlertCircle } from 'lucide-react';

interface TaskListProps {
  tasks: InternalTask[];
  bookingId: number | string;
  isLoading?: boolean;
  error?: Error | null;
}

export function TaskList({ tasks, bookingId, isLoading, error }: TaskListProps) {
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center">
        <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
        <h3 className="text-lg font-semibold text-gray-900">Failed to load tasks</h3>
        <p className="text-sm text-gray-500 mt-2">
          {error.message || 'An unexpected error occurred'}
        </p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <Skeleton className="h-5 w-3/4 mb-2" />
                <Skeleton className="h-4 w-1/2" />
              </div>
              <Skeleton className="h-8 w-24 ml-4" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center">
        <div className="rounded-full bg-gray-100 p-3 mb-4">
          <svg
            className="h-6 w-6 text-gray-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-gray-900">No tasks yet</h3>
        <p className="text-sm text-gray-500 mt-2">
          Create your first task using the form below
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} bookingId={bookingId} />
      ))}
    </div>
  );
}

export default TaskList;
