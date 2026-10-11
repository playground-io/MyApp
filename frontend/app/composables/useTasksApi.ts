// This composable is a small API client for the frontend.
// It centralizes all task-related HTTP requests so the UI does not need to know
// the exact endpoint details everywhere.
import type { Task, TaskCreate, TaskUpdate } from "~/types/task";

export function useTasksApi() {
  // Nuxt exposes environment variables through useRuntimeConfig().
  const config = useRuntimeConfig();

  // `apiBase` points to the backend, for example http://localhost:8000.
  // We add /api because the backend routes are grouped under that prefix.
  const baseURL = `${config.public.apiBase}/api`;

  return {
    // GET /api/tasks => fetch every task.
    list: () => $fetch<Task[]>("/tasks", { baseURL }),

    // POST /api/tasks => create a task.
    create: (payload: TaskCreate) =>
      $fetch<Task>("/tasks", { baseURL, method: "POST", body: payload }),

    // PATCH /api/tasks/:id => update a task's completed state.
    update: (id: number, payload: TaskUpdate) =>
      $fetch<Task>(`/tasks/${id}`, { baseURL, method: "PATCH", body: payload }),

    // DELETE /api/tasks/:id => remove a task.
    remove: (id: number) =>
      $fetch<void>(`/tasks/${id}`, { baseURL, method: "DELETE" }),
  };
}
