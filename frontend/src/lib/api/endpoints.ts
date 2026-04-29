export const API_ENDPOINTS = {
  tasks: (bookingId: number | string) => `/bookings/${bookingId}/tasks/`,
  task: (bookingId: number | string, taskId: number) => 
    `/bookings/${bookingId}/tasks/${taskId}/status`,
} as const;
