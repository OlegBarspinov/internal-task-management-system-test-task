import { render, screen } from '@testing-library/react';
import { TaskStatusBadge } from '@/components/tasks/TaskStatusBadge';
import { TaskStatus } from '@/types';

describe('TaskStatusBadge', () => {
  it('renders OPEN status correctly', () => {
    render(<TaskStatusBadge status="OPEN" />);
    expect(screen.getByText('Open')).toBeInTheDocument();
  });

  it('renders IN_PROGRESS status correctly', () => {
    render(<TaskStatusBadge status="IN_PROGRESS" />);
    expect(screen.getByText('In Progress')).toBeInTheDocument();
  });

  it('renders CLOSED status correctly', () => {
    render(<TaskStatusBadge status="CLOSED" />);
    expect(screen.getByText('Closed')).toBeInTheDocument();
  });

  it('applies correct styling for each status', () => {
    const { rerender } = render(<TaskStatusBadge status="OPEN" />);
    expect(screen.getByText('Open')).toHaveClass('bg-blue-100');

    rerender(<TaskStatusBadge status="IN_PROGRESS" />);
    expect(screen.getByText('In Progress')).toHaveClass('bg-yellow-100');

    rerender(<TaskStatusBadge status="CLOSED" />);
    expect(screen.getByText('Closed')).toHaveClass('bg-green-100');
  });

  it('accepts custom className', () => {
    render(<TaskStatusBadge status="OPEN" className="custom-class" />);
    expect(screen.getByText('Open')).toHaveClass('custom-class');
  });
});
