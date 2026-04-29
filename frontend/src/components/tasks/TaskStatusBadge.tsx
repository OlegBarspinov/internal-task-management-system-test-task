import { cn } from '@/lib/utils';
import { TaskStatus } from '@/types';

interface TaskStatusBadgeProps {
  status: TaskStatus;
  className?: string;
}

const statusConfig: Record<TaskStatus, { label: string; color: string }> = {
  OPEN: {
    label: 'Open',
    color: 'bg-blue-100 text-blue-800 border-blue-200',
  },
  IN_PROGRESS: {
    label: 'In Progress',
    color: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  },
  CLOSED: {
    label: 'Closed',
    color: 'bg-green-100 text-green-800 border-green-200',
  },
};

export function TaskStatusBadge({ status, className }: TaskStatusBadgeProps) {
  const config = statusConfig[status];

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium border',
        config.color,
        className
      )}
    >
      {config.label}
    </span>
  );
}

export default TaskStatusBadge;
