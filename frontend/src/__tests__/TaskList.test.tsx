import { render, screen } from '@testing-library/react';
import { TaskList } from '@/components/tasks/TaskList';
import { InternalTask } from '@/types';
import { describe, it, expect, vi } from 'vitest';

const mockTasks: InternalTask[] = [
  {
    id: 1,
    booking_id: 1,
    title: 'Task 1',
    status: 'OPEN',
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    booking_id: 1,
    title: 'Task 2',
    status: 'CLOSED',
    created_at: '2024-01-02T00:00:00Z',
  },
];

describe('TaskList', () => {
  it('renders loading state', () => {
    render(
      <TaskList 
        tasks={[]} 
        bookingId={1} 
        isLoading={true} 
        error={null} 
      />
    );
    
    // Should show skeletons
    const skeletons = screen.getAllByRole('generic');
    expect(skeletons.length).toBeGreaterThan(0);
  });

  it('renders error state', () => {
    const error = new Error('Failed to load');
    render(
      <TaskList 
        tasks={[]} 
        bookingId={1} 
        isLoading={false} 
        error={error} 
      />
    );
    
    expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
    expect(screen.getByText(error.message)).toBeInTheDocument();
  });

  it('renders empty state when no tasks', () => {
    render(
      <TaskList 
        tasks={[]} 
        bookingId={1} 
        isLoading={false} 
        error={null} 
      />
    );
    
    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    expect(screen.getByText('Create your first task using the form below')).toBeInTheDocument();
  });

  it('renders tasks correctly', () => {
    render(
      <TaskList 
        tasks={mockTasks} 
        bookingId={1} 
        isLoading={false} 
        error={null} 
      />
    );
    
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
  });
});
