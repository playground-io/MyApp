<script setup lang="ts">
import type { Task } from "~/types/task";

type TaskFilter = "all" | "active" | "completed";
const filterOptions: { label: string; value: TaskFilter }[] = [
  { label: "All", value: "all" },
  { label: "To do", value: "active" },
  { label: "Done", value: "completed" },
];

const api = useTasksApi();
const {
  data: tasks,
  error: loadError,
  pending,
  refresh,
} = await useAsyncData<Task[]>("tasks", () => api.list(), {
  server: false,
  default: () => [],
});

const title = ref("");
const description = ref("");
const filter = ref<TaskFilter>("all");
const saving = ref(false);
const updatingId = ref<number | null>(null);
const deletingId = ref<number | null>(null);
const errorMessage = ref("");
const requestError = computed(
  () => errorMessage.value || (loadError.value ? getErrorMessage(loadError.value) : ""),
);

const completedCount = computed(
  () => tasks.value.filter((task) => task.completed).length,
);
const activeCount = computed(() => tasks.value.length - completedCount.value);
const filteredTasks = computed(() =>
  tasks.value.filter((task) => {
    if (filter.value === "active") return !task.completed;
    if (filter.value === "completed") return task.completed;
    return true;
  }),
);

function getErrorMessage(error: unknown) {
  return error instanceof Error
    ? error.message
    : "Something went wrong. Please try again.";
}

function showError(error: unknown) {
  errorMessage.value = getErrorMessage(error);
}

async function createTask() {
  const cleanTitle = title.value.trim();
  if (!cleanTitle || saving.value) return;

  errorMessage.value = "";
  saving.value = true;
  try {
    await api.create({
      title: cleanTitle,
      description: description.value.trim() || null,
    });
    title.value = "";
    description.value = "";
    await refresh();
  } catch (error: unknown) {
    showError(error);
  } finally {
    saving.value = false;
  }
}

async function toggleTask(task: Task) {
  if (updatingId.value !== null) return;

  errorMessage.value = "";
  updatingId.value = task.id;
  try {
    await api.update(task.id, { completed: !task.completed });
    await refresh();
  } catch (error: unknown) {
    showError(error);
  } finally {
    updatingId.value = null;
  }
}

async function deleteTask(task: Task) {
  if (deletingId.value !== null) return;

  errorMessage.value = "";
  deletingId.value = task.id;
  try {
    await api.remove(task.id);
    await refresh();
  } catch (error: unknown) {
    showError(error);
  } finally {
    deletingId.value = null;
  }
}
</script>

<template>
  <main class="mx-auto min-h-screen max-w-5xl px-4 py-10 sm:px-8 sm:py-16">
    <header class="mb-10">
      <p class="mb-3 text-sm font-semibold uppercase tracking-[0.18em] text-primary">
        MyApp starter
      </p>
      <div class="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
        <div>
          <h1 class="text-4xl font-bold tracking-tight text-gray-950 sm:text-5xl">
            Make room for
            <span class="text-primary">what matters.</span>
          </h1>
          <p class="mt-3 max-w-xl text-base leading-7 text-gray-600">
            A simple task tracker to help you get started. Add one thing, then
            take it from there.
          </p>
        </div>
        <div class="flex gap-3">
          <UCard class="min-w-24 text-center">
            <p class="text-2xl font-bold text-gray-950">{{ activeCount }}</p>
            <p class="text-xs text-gray-500">to do</p>
          </UCard>
          <UCard class="min-w-24 text-center">
            <p class="text-2xl font-bold text-gray-950">{{ completedCount }}</p>
            <p class="text-xs text-gray-500">done</p>
          </UCard>
        </div>
      </div>
    </header>

    <UCard class="mb-8">
      <template #header>
        <div>
          <h2 class="text-lg font-semibold text-gray-950">Add a task</h2>
          <p class="mt-1 text-sm text-gray-500">Start with a small, clear next step.</p>
        </div>
      </template>

      <form class="space-y-4" @submit.prevent="createTask">
        <UInput
          v-model="title"
          aria-label="Task title"
          autocomplete="off"
          maxlength="200"
          placeholder="What needs to get done?"
          required
          size="lg"
        />
        <UTextarea
          v-model="description"
          aria-label="Task description"
          maxlength="2000"
          placeholder="Add a note (optional)"
          :rows="2"
        />
        <div class="flex justify-end">
          <UButton type="submit" :loading="saving" :disabled="!title.trim()">
            Add task
          </UButton>
        </div>
      </form>
    </UCard>

    <section aria-labelledby="tasks-heading">
      <div class="mb-4 flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h2 id="tasks-heading" class="text-xl font-semibold text-gray-950">
            Your tasks
          </h2>
          <p class="mt-1 text-sm text-gray-500" aria-live="polite">
            {{ tasks.length }} {{ tasks.length === 1 ? "task" : "tasks" }} in your list
          </p>
        </div>
        <div class="flex gap-2" aria-label="Filter tasks">
          <UButton
            v-for="option in filterOptions"
            :key="option.value"
            size="sm"
            :variant="filter === option.value ? 'solid' : 'ghost'"
            :color="filter === option.value ? 'primary' : 'neutral'"
            @click="filter = option.value"
          >
            {{ option.label }}
          </UButton>
        </div>
      </div>

      <div
        v-if="requestError"
        class="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-lg bg-red-50 p-3 text-sm text-red-700"
        role="alert"
      >
        <p>{{ requestError }}</p>
        <UButton size="sm" color="error" variant="ghost" @click="refresh()">
          Try again
        </UButton>
      </div>

      <div v-if="pending" class="py-12 text-center text-sm text-gray-500" role="status">
        Loading your tasks…
      </div>
      <div
        v-else-if="loadError && tasks.length === 0"
        class="rounded-2xl border border-dashed border-red-200 bg-white/70 px-6 py-14 text-center"
      >
        <p class="text-lg font-medium text-gray-800">Could not load your tasks.</p>
        <p class="mt-2 text-sm text-gray-500">Check that the API is running, then try again.</p>
      </div>
      <div
        v-else-if="filteredTasks.length === 0"
        class="rounded-2xl border border-dashed border-gray-300 bg-white/70 px-6 py-14 text-center"
      >
        <p class="text-lg font-medium text-gray-800">
          {{ tasks.length === 0 ? "A fresh start." : "Nothing in this view." }}
        </p>
        <p class="mt-2 text-sm text-gray-500">
          {{ tasks.length === 0 ? "Add your first task above and make it happen." : "Try another filter to see your tasks." }}
        </p>
      </div>
      <ul v-else class="space-y-3">
        <li v-for="task in filteredTasks" :key="task.id">
          <UCard>
            <div class="flex items-start gap-4">
              <UButton
                class="mt-0.5 shrink-0"
                size="sm"
                :color="task.completed ? 'success' : 'neutral'"
                :variant="task.completed ? 'solid' : 'outline'"
                :aria-label="task.completed ? `Mark ${task.title} as to do` : `Complete ${task.title}`"
                :loading="updatingId === task.id"
                :disabled="updatingId !== null"
                @click="toggleTask(task)"
              >
                {{ task.completed ? "Done" : "Mark done" }}
              </UButton>
              <div class="min-w-0 flex-1">
                <p
                  class="font-medium text-gray-900"
                  :class="{ 'text-gray-400 line-through': task.completed }"
                >
                  {{ task.title }}
                </p>
                <p v-if="task.description" class="mt-1 whitespace-pre-wrap text-sm text-gray-500">
                  {{ task.description }}
                </p>
                <p class="mt-2 text-xs text-gray-400">
                  Added {{ new Date(task.created_at).toLocaleDateString() }}
                </p>
              </div>
              <UButton
                color="error"
                variant="ghost"
                size="sm"
                :aria-label="`Delete ${task.title}`"
                :loading="deletingId === task.id"
                :disabled="deletingId !== null"
                @click="deleteTask(task)"
              >
                Delete
              </UButton>
            </div>
          </UCard>
        </li>
      </ul>
    </section>
  </main>
</template>
