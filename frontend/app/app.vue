<template>
  <UApp>
    <div class="min-h-screen">
      <header class="border-b border-gray-200/80 bg-white/80 backdrop-blur">
        <nav
          class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-8"
          aria-label="Main navigation"
        >
          <NuxtLink to="/" class="flex items-center gap-3" aria-label="MyApp home">
            <span
              class="flex size-9 items-center justify-center rounded-xl bg-primary text-white"
              aria-hidden="true"
            >
              <UIcon name="i-lucide-chart-no-axes-combined" class="size-5" />
            </span>
            <span class="text-lg font-bold tracking-tight text-gray-950">myapp<span class="text-primary">.</span></span>
          </NuxtLink>

          <div class="flex h-full items-center gap-1">
            <NuxtLink
              to="/"
              class="flex h-full items-center border-b-2 px-4 text-sm font-medium transition-colors"
              :class="$route.path === '/' ? 'border-primary text-primary' : 'border-transparent text-gray-500 hover:text-gray-900'"
              :aria-current="$route.path === '/' ? 'page' : undefined"
            >
              <UIcon name="i-lucide-layout-dashboard" class="mr-2 size-4" />
              Overview
            </NuxtLink>
            <NuxtLink
              to="/tasks"
              class="flex h-full items-center border-b-2 px-4 text-sm font-medium transition-colors"
              :class="$route.path === '/tasks' ? 'border-primary text-primary' : 'border-transparent text-gray-500 hover:text-gray-900'"
              :aria-current="$route.path === '/tasks' ? 'page' : undefined"
            >
              <UIcon name="i-lucide-list-checks" class="mr-2 size-4" />
              Tasks
            </NuxtLink>
          </div>

          <div class="flex items-center gap-2 rounded-full bg-gray-100 py-1 pl-1 pr-3">
            <UAvatar text="JD" size="xs" />
            <span class="hidden text-xs font-medium text-gray-600 sm:inline">Demo workspace</span>
          </div>
        </nav>
      </header>

      <NuxtPage />
    </div>
  </UApp>
</template>
