import { createTaskSchema, updateTaskStatusSchema } from '@/lib/validation/schemas';
import { z } from 'zod';

describe('Validation Schemas', () => {
  describe('createTaskSchema', () => {
    it('accepts valid title', () => {
      const result = createTaskSchema.safeParse({ title: 'My Task' });
      expect(result.success).toBe(true);
    });

    it('rejects empty title', () => {
      const result = createTaskSchema.safeParse({ title: '' });
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0].message).toBe('Title is required');
      }
    });

    it('rejects title longer than 255 characters', () => {
      const longTitle = 'a'.repeat(256);
      const result = createTaskSchema.safeParse({ title: longTitle });
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0].message).toBe(
          'Title must be less than 255 characters'
        );
      }
    });

    it('trims whitespace from title', () => {
      const result = createTaskSchema.safeParse({ title: '  My Task  ' });
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.title).toBe('My Task');
      }
    });
  });

  describe('updateTaskStatusSchema', () => {
    it('accepts valid status values', () => {
      const validStatuses = ['OPEN', 'IN_PROGRESS', 'CLOSED'] as const;
      
      validStatuses.forEach((status) => {
        const result = updateTaskStatusSchema.safeParse({ status });
        expect(result.success).toBe(true);
        if (result.success) {
          expect(result.data.status).toBe(status);
        }
      });
    });

    it('rejects invalid status value', () => {
      const result = updateTaskStatusSchema.safeParse({ status: 'INVALID' });
      expect(result.success).toBe(false);
    });
  });
});
