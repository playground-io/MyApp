// This file defines the TypeScript shape of a task.
// TypeScript helps the frontend catch mistakes before they happen.
// A task is the same data the backend returns from the API.
export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
}

// Data needed to create a new task.
export interface TaskCreate {
  title: string;
  description?: string | null;
}

// Data used when changing a task's completion state.
export interface TaskUpdate {
  completed: boolean;
}
