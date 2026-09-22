const API_BASE = "/api/tasks";
const POLL_INTERVAL_MS = 3000;

let tasks = [];
let editingId = null;

const taskListEl = document.getElementById("taskList");
const taskFormEl = document.getElementById("taskForm");
const titleInputEl = document.getElementById("titleInput");
const dueAtInputEl = document.getElementById("dueAtInput");
const statusInputEl = document.getElementById("statusInput");

const editModalEl = document.getElementById("editModal");
const editFormEl = document.getElementById("editForm");
const editIdEl = document.getElementById("editId");
const editTitleEl = document.getElementById("editTitle");
const editDescriptionEl = document.getElementById("editDescription");
const editDueAtEl = document.getElementById("editDueAt");
const editStatusEl = document.getElementById("editStatus");
const cancelEditEl = document.getElementById("cancelEdit");

const themeToggleEl = document.getElementById("themeToggle");

const STATUS_LABELS = {
  todo: { text: "todo", cls: "bg-slate-200 text-slate-700 dark:bg-slate-600 dark:text-slate-100" },
  in_progress: { text: "in_progress", cls: "bg-amber-200 text-amber-800 dark:bg-amber-500/30 dark:text-amber-200" },
  done: { text: "done", cls: "bg-emerald-200 text-emerald-800 dark:bg-emerald-500/30 dark:text-emerald-200" },
};

function initTheme() {
  const saved = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const isDark = saved ? saved === "dark" : prefersDark;
  document.documentElement.classList.toggle("dark", isDark);
  themeToggleEl.textContent = isDark ? "☀️" : "🌙";
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle("dark");
  localStorage.setItem("theme", isDark ? "dark" : "light");
  themeToggleEl.textContent = isDark ? "☀️" : "🌙";
}

function localToUtcIso(localValue) {
  if (!localValue) return null;
  return new Date(localValue).toISOString();
}

function utcToLocalInputValue(utcValue) {
  if (!utcValue) return "";
  const date = new Date(utcValue);
  const offsetMs = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - offsetMs).toISOString().slice(0, 16);
}

function formatRemaining(dueAt) {
  if (!dueAt) return "마감 없음";
  const diffMs = new Date(dueAt).getTime() - Date.now();
  if (diffMs <= 0) return "마감 지남";
  const minutes = Math.floor(diffMs / 60000);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  if (days > 0) return `${days}일 남음`;
  if (hours > 0) return `${hours}시간 남음`;
  return `${minutes}분 남음`;
}

async function fetchTasks() {
  const response = await fetch(API_BASE);
  tasks = await response.json();
  renderTasks();
}

function renderTasks() {
  taskListEl.innerHTML = "";
  tasks.forEach((task) => {
    const badge = STATUS_LABELS[task.status] || STATUS_LABELS.todo;
    const card = document.createElement("div");
    card.className =
      "bg-white/70 dark:bg-white/10 glass rounded-2xl shadow-md p-4 flex items-center justify-between cursor-pointer hover:shadow-lg transition-shadow";
    card.innerHTML = `
      <div class="min-w-0">
        <p class="font-medium truncate">${escapeHtml(task.title)}</p>
        <div class="flex items-center gap-2 mt-1">
          <span class="text-xs px-2 py-0.5 rounded-full ${badge.cls}">${badge.text}</span>
          <span class="text-xs text-slate-500 dark:text-slate-400">${formatRemaining(task.due_at)}</span>
        </div>
      </div>
      <button data-id="${task.id}" class="deleteBtn shrink-0 ml-3 w-9 h-9 rounded-full bg-white/70 dark:bg-white/10 shadow flex items-center justify-center">🗑️</button>
    `;
    card.addEventListener("click", (e) => {
      if (e.target.closest(".deleteBtn")) return;
      openEditModal(task.id);
    });
    card.querySelector(".deleteBtn").addEventListener("click", () => deleteTask(task.id));
    taskListEl.appendChild(card);
  });
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

async function createTask(event) {
  event.preventDefault();
  const payload = {
    title: titleInputEl.value,
    status: statusInputEl.value,
    due_at: localToUtcIso(dueAtInputEl.value),
  };
  await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  taskFormEl.reset();
  await fetchTasks();
}

async function openEditModal(id) {
  const response = await fetch(`${API_BASE}/${id}`);
  const task = await response.json();
  editingId = task.id;
  editIdEl.value = task.id;
  editTitleEl.value = task.title;
  editDescriptionEl.value = task.description || "";
  editStatusEl.value = task.status;
  editDueAtEl.value = utcToLocalInputValue(task.due_at);
  editModalEl.classList.remove("hidden");
}

function closeEditModal() {
  editModalEl.classList.add("hidden");
  editingId = null;
}

async function submitEdit(event) {
  event.preventDefault();
  const payload = {
    title: editTitleEl.value,
    description: editDescriptionEl.value || null,
    status: editStatusEl.value,
    due_at: localToUtcIso(editDueAtEl.value),
  };
  await fetch(`${API_BASE}/${editingId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  closeEditModal();
  await fetchTasks();
}

async function deleteTask(id) {
  if (!confirm("이 할 일을 삭제할까요?")) return;
  await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
  await fetchTasks();
}

taskFormEl.addEventListener("submit", createTask);
editFormEl.addEventListener("submit", submitEdit);
cancelEditEl.addEventListener("click", closeEditModal);
themeToggleEl.addEventListener("click", toggleTheme);

initTheme();
fetchTasks();
setInterval(fetchTasks, POLL_INTERVAL_MS);
