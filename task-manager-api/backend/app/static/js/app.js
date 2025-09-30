document.addEventListener('DOMContentLoaded', async () => {
  const container = document.getElementById('tasks');
  if(!container) return;
  container.innerHTML = '<em>Loading tasks...</em>';
  try{
    const res = await fetch('/api/v1/tasks', { headers: { 'accept': 'application/json' } });
    if(!res.ok){
      container.innerHTML = 'Please login via API to view tasks.';
      return;
    }
    const data = await res.json();
    container.innerHTML = (data||[]).map(t => `<div>${t.title} ${t.is_completed ? '✅' : ''}</div>`).join('');
  }catch(err){
    container.innerHTML = 'Failed to load tasks.';
  }
});


