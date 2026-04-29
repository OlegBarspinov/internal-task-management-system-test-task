'use client';

import { useTasks } from '@/hooks/api/useTasks';
import { TaskList } from '@/components/tasks/TaskList';
import { CreateTaskForm } from '@/components/tasks/CreateTaskForm';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface BookingPageProps {
  params: {
    bookingId: string;
  };
}

export default function BookingPage({ params }: BookingPageProps) {
  const bookingId = params.bookingId;
  const router = useRouter();
  
  const {
    data: tasks = [],
    isLoading,
    error,
    refetch,
  } = useTasks({
    bookingId,
    enabled: !!bookingId,
  });

  const handleTaskCreated = () => {
    // Invalidate and refetch tasks
    refetch();
  };

  if (!bookingId) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center">
        <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
        <h3 className="text-lg font-semibold text-gray-900">Invalid Booking ID</h3>
        <p className="text-sm text-gray-500 mt-2">
          Booking ID is required
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Tasks List */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Tasks</CardTitle>
            </CardHeader>
            <CardContent>
              <TaskList
                tasks={tasks}
                bookingId={bookingId}
                isLoading={isLoading}
                error={error}
              />
            </CardContent>
          </Card>
        </div>

        {/* Create Task Form */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Create New Task</CardTitle>
            </CardHeader>
            <CardContent>
              <CreateTaskForm
                bookingId={bookingId}
                onSuccess={handleTaskCreated}
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
