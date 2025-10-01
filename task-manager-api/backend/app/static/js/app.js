// API Base URL
const API_BASE = '/api/v1/tasks';

// DOM Elements
const tasksContainer = document.getElementById('tasks-list');
const loadingDiv = document.getElementById('tasks-loading');
const modal = document.getElementById('task-modal');
const taskForm = document.getElementById('task-form');
const modalTitle = document.getElementById('modal-title');
const addTaskBtn = document.getElementById('add-task-btn');
const cancelBtn = document.getElementById('cancel-btn');
const closeBtn = document.querySelector('.close');

// State
let currentTaskId = null;
let tasks = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadTasks();
  setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
  addTaskBtn.addEventListener('click', () => openModal());
  cancelBtn.addEventListener('click', () => closeModal());
  closeBtn.addEventListener('click', () => closeModal());
  taskForm.addEventListener('submit', handleFormSubmit);
  
  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });
}

// API Functions
async function loadTasks() {
  try {
    loadingDiv.style.display = 'block';
    const response = await fetch(API_BASE);
    if (!response.ok) throw new Error('Failed to load tasks');
    
    tasks = await response.json();
    renderTasks();
  } catch (error) {
    tasksContainer.innerHTML = '<div class="error">Failed to load tasks</div>';
  } finally {
    loadingDiv.style.display = 'none';
  }
}

async function createTask(taskData) {
  const response = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData)
  });
  if (!response.ok) throw new Error('Failed to create task');
  return response.json();
}

async function updateTask(id, taskData) {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData)
  });
  if (!response.ok) throw new Error('Failed to update task');
  return response.json();
}

async function deleteTask(id) {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: 'DELETE'
  });
  if (!response.ok) throw new Error('Failed to delete task');
}

// UI Functions
function renderTasks() {
  if (tasks.length === 0) {
    tasksContainer.innerHTML = '<div class="empty-state">No tasks yet. Add your first task!</div>';
    return;
  }
  
  tasksContainer.innerHTML = tasks.map(task => `
    <div class="task-card ${task.is_completed ? 'completed' : ''}" onclick="editTask(${task.id})">
      <div class="task-content">
        <h3 class="task-title">${escapeHtml(task.title)}</h3>
      </div>
      <div class="task-actions">
        <button class="btn btn-sm ${task.is_completed ? 'btn-secondary' : 'btn-success'}" 
                onclick="event.stopPropagation(); toggleTask(${task.id}, ${!task.is_completed})">
          ${task.is_completed ? 'Undo' : 'Complete'}
        </button>
        <button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); editTask(${task.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="event.stopPropagation(); deleteTaskConfirm(${task.id})">Delete</button>
      </div>
    </div>
  `).join('');
}

function openModal(taskId = null) {
  currentTaskId = taskId;
  if (taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
      modalTitle.textContent = 'Edit Task';
      populateForm(task);
    }
  } else {
    modalTitle.textContent = 'Add New Task';
    taskForm.reset();
    document.getElementById('task-id').value = '';
  }
  modal.style.display = 'block';
}

function closeModal() {
  modal.style.display = 'none';
  currentTaskId = null;
  taskForm.reset();
}

function populateForm(task) {
  document.getElementById('task-id').value = task.id;
  document.getElementById('title').value = task.title;
  document.getElementById('description').value = task.description || '';
  document.getElementById('priority').value = task.priority;
  document.getElementById('due-date').value = task.due_date ? formatDateForInput(task.due_date) : '';
}

async function handleFormSubmit(e) {
  e.preventDefault();
  
  const formData = new FormData(taskForm);
  const taskData = {
    title: formData.get('title'),
    description: formData.get('description') || null,
    priority: parseInt(formData.get('priority')),
    due_date: formData.get('due_date') || null
  };
  
  try {
    if (currentTaskId) {
      await updateTask(currentTaskId, taskData);
    } else {
      await createTask(taskData);
    }
    closeModal();
    loadTasks();
  } catch (error) {
    alert('Error saving task: ' + error.message);
  }
}

async function toggleTask(id, isCompleted) {
  try {
    await updateTask(id, { is_completed: isCompleted });
    loadTasks();
  } catch (error) {
    alert('Error updating task: ' + error.message);
  }
}

function editTask(id) {
  openModal(id);
}

async function deleteTaskConfirm(id) {
  if (confirm('Are you sure you want to delete this task?')) {
    try {
      await deleteTask(id);
      loadTasks();
    } catch (error) {
      alert('Error deleting task: ' + error.message);
    }
  }
}

// Utility Functions
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function getPriorityText(priority) {
  const priorities = ['Low', 'Medium', 'High'];
  return priorities[priority] || 'Low';
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString();
}

function formatDateForInput(dateString) {
  const date = new Date(dateString);
  return date.toISOString().slice(0, 16);
}