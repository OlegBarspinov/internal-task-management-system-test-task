'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useCreateTask } from '@/hooks/api/useCreateTask';
import { createTaskSchema, type CreateTaskInput } from '@/lib/validation/schemas';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertCircle, CheckCircle2 } from 'lucide-react';
import { useState } from 'react';

interface CreateTaskFormProps {
  bookingId: number | string;
  onSuccess?: () => void;
}

export function CreateTaskForm({ bookingId, onSuccess }: CreateTaskFormProps) {
  const [error, setError] = useState<string | null>(null);
  
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateTaskInput>({
    resolver: zodResolver(createTaskSchema),
  });

  const createTaskMutation = useCreateTask({
    bookingId,
    onSuccess: () => {
      reset();
      setError(null);
      onSuccess?.();
    },
    onError: (err) => {
      if (err.response?.status === 409) {
        setError('A task with this title already exists for this booking');
      } else {
        setError('Failed to create task. Please try again.');
      }
    },
  });

  const onSubmit = async (data: CreateTaskInput) => {
    setError(null);
    try {
      await createTaskMutation.mutateAsync(data);
    } catch {
      // Error is handled in onError
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="title">Task Title</Label>
        <Input
          id="title"
          placeholder="Enter task title"
          {...register('title')}
          disabled={isSubmitting || createTaskMutation.isPending}
          className={errors.title ? 'border-red-500' : ''}
        />
        {errors.title && (
          <p className="text-sm text-red-600 flex items-center gap-1">
            <AlertCircle className="h-4 w-4" />
            {errors.title.message}
          </p>
        )}
      </div>

      {error && (
        <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-700">
          <AlertCircle className="h-4 w-4" />
          {error}
        </div>
      )}

      <Button
        type="submit"
        disabled={isSubmitting || createTaskMutation.isPending}
        className="w-full"
      >
        {createTaskMutation.isPending ? (
          <>
            <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2" />
            Creating...
          </>
        ) : (
          'Create Task'
        )}
      </Button>
    </form>
  );
}

export default CreateTaskForm;
