import { formatDate, getStatusColor, cn } from '@/lib/utils';

describe('Utils', () => {
  describe('formatDate', () => {
    it('formats date correctly', () => {
      const dateString = '2024-01-15T10:30:00Z';
      const formatted = formatDate(dateString);
      expect(formatted).toContain('Jan');
      expect(formatted).toContain('15');
      expect(formatted).toContain('2024');
    });
  });

  describe('getStatusColor', () => {
    it('returns correct color for OPEN status', () => {
      expect(getStatusColor('OPEN')).toBe('bg-blue-100 text-blue-800');
    });

    it('returns correct color for IN_PROGRESS status', () => {
      expect(getStatusColor('IN_PROGRESS')).toBe('bg-yellow-100 text-yellow-800');
    });

    it('returns correct color for CLOSED status', () => {
      expect(getStatusColor('CLOSED')).toBe('bg-green-100 text-green-800');
    });

    it('returns default color for unknown status', () => {
      expect(getStatusColor('UNKNOWN')).toBe('bg-gray-100 text-gray-800');
    });
  });

  describe('cn', () => {
    it('merges class names correctly', () => {
      const result = cn('class1', 'class2', 'class3');
      expect(result).toBe('class1 class2 class3');
    });

    it('handles conditional classes', () => {
      const result = cn('base', false && 'hidden', 'always');
      expect(result).toBe('base always');
    });

    it('merges Tailwind classes correctly with conflicts', () => {
      const result = cn('px-4 py-2', 'px-6');
      expect(result).toBe('py-2 px-6');
    });
  });
});
