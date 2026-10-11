<script setup lang="ts">
type TimeRange = "24h" | "7d" | "30d";

const selectedRange = ref<TimeRange>("24h");
const rangeOptions: { label: string; value: TimeRange }[] = [
  { label: "Last 24 hours", value: "24h" },
  { label: "Last 7 days", value: "7d" },
  { label: "Last 30 days", value: "30d" },
];

const chartSeries: Record<
  TimeRange,
  { labels: string[]; requests: number[]; previous: number[] }
> = {
  "24h": {
    labels: ["12 AM", "4 AM", "8 AM", "12 PM", "4 PM", "8 PM", "Now"],
    requests: [38, 29, 43, 35, 62, 53, 78, 68, 91, 74, 84, 65, 80],
    previous: [27, 37, 31, 46, 42, 54, 48, 57, 63, 51, 68, 59, 64],
  },
  "7d": {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    requests: [48, 58, 44, 72, 66, 84, 76, 94, 69, 82, 74, 91, 100],
    previous: [35, 47, 43, 56, 49, 64, 58, 71, 61, 74, 65, 79, 73],
  },
  "30d": {
    labels: ["Sep 12", "Sep 17", "Sep 22", "Sep 27", "Oct 2", "Oct 7", "Oct 11"],
    requests: [24, 33, 30, 45, 39, 57, 52, 68, 59, 74, 66, 89, 96],
    previous: [31, 27, 38, 32, 47, 40, 54, 48, 61, 55, 68, 62, 72],
  },
};

const metrics = [
  {
    label: "Active users",
    value: "24,816",
    change: "+12.8%",
    direction: "up",
    icon: "i-lucide-users",
    tone: "bg-blue-50 text-blue-600",
    caption: "vs. previous period",
  },
  {
    label: "Requests / sec",
    value: "1,284",
    change: "+8.2%",
    direction: "up",
    icon: "i-lucide-activity",
    tone: "bg-violet-50 text-violet-600",
    caption: "vs. previous period",
  },
  {
    label: "Avg. latency",
    value: "128 ms",
    change: "−14 ms",
    direction: "down",
    icon: "i-lucide-gauge",
    tone: "bg-amber-50 text-amber-600",
    caption: "vs. previous period",
  },
  {
    label: "Error rate",
    value: "0.24%",
    change: "−0.08%",
    direction: "down",
    icon: "i-lucide-circle-check",
    tone: "bg-emerald-50 text-emerald-600",
    caption: "vs. previous period",
  },
];

const services = [
  { name: "API Gateway", region: "us-east-1", uptime: "99.99%", latency: "42 ms" },
  { name: "Application Server", region: "us-east-1", uptime: "99.95%", latency: "86 ms" },
  { name: "Database", region: "us-east-1", uptime: "99.98%", latency: "12 ms" },
  { name: "Background Jobs", region: "us-west-2", uptime: "99.91%", latency: "—" },
];

const events: {
  name: string;
  detail: string;
  time: string;
  status: string;
  tone: "success" | "warning";
}[] = [
  { name: "POST /api/checkout", detail: "Request completed", time: "2 sec ago", status: "200", tone: "success" },
  { name: "GET /api/products", detail: "Request completed", time: "8 sec ago", status: "200", tone: "success" },
  { name: "POST /api/webhooks", detail: "Request throttled", time: "14 sec ago", status: "429", tone: "warning" },
  { name: "GET /api/users/me", detail: "Request completed", time: "21 sec ago", status: "200", tone: "success" },
  { name: "PATCH /api/settings", detail: "Request completed", time: "34 sec ago", status: "200", tone: "success" },
];

const currentSeries = computed(() => chartSeries[selectedRange.value]);

function points(values: number[]) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const spread = max - min || 1;

  return values
    .map((value, index) => {
      const x = (index / (values.length - 1)) * 900;
      const y = 210 - ((value - min) / spread) * 170;
      return `${x},${y}`;
    })
    .join(" ");
}
</script>

<template>
  <main class="mx-auto max-w-7xl px-4 py-8 sm:px-8 sm:py-10">
    <section class="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
      <div>
        <div class="mb-2 flex items-center gap-2">
          <span class="size-2 rounded-full bg-emerald-500 ring-4 ring-emerald-100" />
          <p class="text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700">
            All systems operational
          </p>
        </div>
        <h1 class="text-3xl font-bold tracking-tight text-gray-950 sm:text-4xl">
          Good morning, Jamie
        </h1>
        <p class="mt-2 text-sm text-gray-500">
          Here’s what’s happening across your workspace.
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-3">
        <UBadge color="warning" variant="subtle" size="lg">
          <UIcon name="i-lucide-flask-conical" class="mr-1.5 size-3.5" />
          Demo data
        </UBadge>
        <label class="sr-only" for="time-range">Dashboard time range</label>
        <select
          id="time-range"
          v-model="selectedRange"
          class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-sm outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
        >
          <option v-for="option in rangeOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>
    </section>

    <div
      class="mb-6 flex items-start gap-3 rounded-xl border border-amber-200/80 bg-amber-50/80 px-4 py-3 text-sm text-amber-900"
      role="note"
    >
      <UIcon name="i-lucide-info" class="mt-0.5 size-4 shrink-0" />
      <p>
        Sample telemetry for preview only. These values are static mock data and
        are not connected to your API or infrastructure.
      </p>
    </div>

    <section class="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4" aria-label="Key metrics">
      <UCard v-for="metric in metrics" :key="metric.label" class="overflow-hidden">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">{{ metric.label }}</p>
            <p class="mt-3 text-3xl font-bold tracking-tight text-gray-950">
              {{ metric.value }}
            </p>
          </div>
          <span class="flex size-10 items-center justify-center rounded-xl" :class="metric.tone">
            <UIcon :name="metric.icon" class="size-5" />
          </span>
        </div>
        <div class="mt-4 flex items-center gap-2">
          <span class="inline-flex items-center gap-1 text-xs font-semibold text-emerald-700">
            <UIcon
              :name="metric.direction === 'up' ? 'i-lucide-trending-up' : 'i-lucide-trending-down'"
              class="size-3.5"
            />
            {{ metric.change }}
          </span>
          <span class="text-xs text-gray-400">{{ metric.caption }}</span>
        </div>
      </UCard>
    </section>

    <section class="mb-6 grid gap-6 xl:grid-cols-[minmax(0,1.7fr)_minmax(300px,0.8fr)]">
      <UCard>
        <template #header>
          <div class="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 class="font-semibold text-gray-950">Request volume</h2>
              <p class="mt-1 text-sm text-gray-500">Incoming requests over time</p>
            </div>
            <div class="flex items-center gap-4 text-xs text-gray-500">
              <span class="flex items-center gap-2">
                <span class="size-2 rounded-full bg-primary" />
                This period
              </span>
              <span class="flex items-center gap-2">
                <span class="size-2 rounded-full bg-gray-300" />
                Previous
              </span>
            </div>
          </div>
        </template>
        <div class="px-1 pb-2">
          <div class="mb-2 flex items-baseline gap-2">
            <span class="text-2xl font-bold tracking-tight text-gray-950">1,284</span>
            <span class="text-sm text-gray-500">requests / sec</span>
          </div>
          <div class="w-full overflow-hidden">
            <svg
              class="h-56 w-full overflow-visible"
              viewBox="0 0 900 250"
              preserveAspectRatio="none"
              role="img"
              :aria-label="`Request volume sample chart for the last ${selectedRange === '24h' ? '24 hours' : selectedRange === '7d' ? '7 days' : '30 days'}`"
            >
              <defs>
                <linearGradient id="traffic-fill" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stop-color="#6366f1" stop-opacity="0.18" />
                  <stop offset="100%" stop-color="#6366f1" stop-opacity="0" />
                </linearGradient>
              </defs>
              <line v-for="y in [40, 82, 124, 166, 208]" :key="y" x1="0" :y1="y" x2="900" :y2="y" stroke="#e5e7eb" stroke-dasharray="4 6" />
              <polygon :points="`0,230 ${points(currentSeries.requests)} 900,230`" fill="url(#traffic-fill)" />
              <polyline
                :points="points(currentSeries.previous)"
                fill="none"
                stroke="#cbd5e1"
                stroke-width="3"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-dasharray="7 8"
                vector-effect="non-scaling-stroke"
              />
              <polyline
                :points="points(currentSeries.requests)"
                fill="none"
                stroke="#6366f1"
                stroke-width="3"
                stroke-linecap="round"
                stroke-linejoin="round"
                vector-effect="non-scaling-stroke"
              />
            </svg>
            <div class="mt-2 flex justify-between text-[11px] text-gray-400">
              <span v-for="label in currentSeries.labels" :key="label">{{ label }}</span>
            </div>
          </div>
        </div>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-start justify-between">
            <div>
              <h2 class="font-semibold text-gray-950">Service health</h2>
              <p class="mt-1 text-sm text-gray-500">Current service status</p>
            </div>
            <UBadge color="success" variant="subtle">All healthy</UBadge>
          </div>
        </template>
        <ul class="divide-y divide-gray-100">
          <li v-for="service in services" :key="service.name" class="flex items-center gap-3 py-3.5 first:pt-0 last:pb-0">
            <span class="relative flex size-2.5 shrink-0">
              <span class="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-20" />
              <span class="relative inline-flex size-2.5 rounded-full bg-emerald-500" />
            </span>
            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-medium text-gray-800">{{ service.name }}</p>
              <p class="mt-0.5 text-xs text-gray-400">{{ service.region }} · {{ service.uptime }} uptime</p>
            </div>
            <span class="shrink-0 text-xs font-medium tabular-nums text-gray-500">{{ service.latency }}</span>
          </li>
        </ul>
      </UCard>
    </section>

    <UCard>
      <template #header>
        <div class="flex items-center justify-between gap-3">
          <div>
            <h2 class="font-semibold text-gray-950">Recent activity</h2>
            <p class="mt-1 text-sm text-gray-500">A sample of recent API requests</p>
          </div>
          <UBadge color="neutral" variant="subtle">Sample feed</UBadge>
        </div>
      </template>
      <div class="overflow-x-auto">
        <table class="w-full min-w-[520px] text-left text-sm">
          <thead>
            <tr class="border-b border-gray-100 text-xs font-medium uppercase tracking-wide text-gray-400">
              <th scope="col" class="pb-3 pr-4">Request</th>
              <th scope="col" class="pb-3 pr-4">Status</th>
              <th scope="col" class="pb-3 pr-4">Result</th>
              <th scope="col" class="pb-3 text-right">When</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="event in events" :key="`${event.name}-${event.time}`">
              <td class="py-3.5 pr-4 font-mono text-xs font-medium text-gray-800">
                {{ event.name }}
              </td>
              <td class="py-3.5 pr-4">
                <UBadge :color="event.tone" variant="subtle" size="sm">{{ event.status }}</UBadge>
              </td>
              <td class="py-3.5 pr-4 text-gray-500">{{ event.detail }}</td>
              <td class="py-3.5 text-right text-xs tabular-nums text-gray-400">{{ event.time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </UCard>
  </main>
</template>
