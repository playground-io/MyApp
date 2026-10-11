import type { Task, TaskCreate, TaskUpdate } from "~/types/task";

export function useTasksApi() {
  const config = useRuntimeConfig();
  const baseURL = `${config.public.apiBase}/api`;

  return {
    list: () => $fetch<Task[]>("/tasks", { baseURL }),
    create: (payload: TaskCreate) =>
      $fetch<Task>("/tasks", { baseURL, method: "POST", body: payload }),
    update: (id: number, payload: TaskUpdate) =>
      $fetch<Task>(`/tasks/${id}`, { baseURL, method: "PATCH", body: payload }),
    remove: (id: number) =>
      $fetch<void>(`/tasks/${id}`, { baseURL, method: "DELETE" }),
  };
}
