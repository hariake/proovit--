import { useState, useEffect } from "react";
import { DndContext, type DragEndEvent, closestCenter } from "@dnd-kit/core";
import { useAuth } from "../context/useAuth";
import Column from "../components/Column";
import TaskModal from "../components/TaskModal";
import { type Task } from "../components/TaskCard";
import api from "../api/client";

const  STATUSES = ["todo", "being_done", "done"]; // Column statuses, must match the backend task statuses


export default function Dashboard() {
    const { user, logout } = useAuth(); // Gets user and logout function from auth context using useAuth hook
    const [tasks, setTasks] = useState<Task[]>([]); // State for tasks, initially empty
    const [selectedTask, setSelectedTask] = useState<Task | null>(null); // State for currently selected task, used for showing task details in modal
    const [showModal, setShowModal] = useState(false); // State for whether task details modal is open
    const [filter, setFilter] = useState<'all' | 'mine' | 'done'>('all'); // State for task filter, can be 'all', 'mine' or 'done', defaults to 'all';
    
    const fetchTasks = async () => { 
        const res = await api.get("/tasks"); // Fetches tasks from backend
        setTasks(res.data.tasks); // Updates tasks state with fetched tasks
    }

    useEffect(() => {
        fetchTasks(); // Fetches tasks on component mount
    }, []); // eslint-disable-line react-hooks/exhaustive-deps


    const filteredTasks = tasks.filter(t => { // Filters tasks based on the selected filter option
        if (filter === 'mine') return t.user_id === user?.user_id; // If filter is 'mine', only show tasks created by the current user
        if (filter === 'done') return t.status === "done"; // If filter is 'done', only show tasks with status "done"
        return true; // If filter is 'all', show all tasks
    });

    const [toast, setToast] = useState<string | null>(null); // State for showing temporary toast messages, will be used to show dragging error message.

    const showToast = (message: string) => { // Function to show a toast message for 2 seconds
        setToast(message);
        setTimeout(() => setToast(null), 2000);
    }

    const handleDragEnd = async (event: DragEndEvent) => { // Handles end of drag-and-drop action
        const { active, over } = event;
        if (!over) return; // If not dropped over a valid droppable area, do nothing

        const taskId = Number(active.id); // Gets the ID of the dragged task
        const newStatus = over.id as string; // Gets the ID of the droppable area it was dropped over, which is the new status

        if (!STATUSES.includes(newStatus)) return; // If new status is not valid, do nothing

        const task = tasks.find(t => t.id === taskId); // Finds the task object that was dragged
        if (!task || task.status === newStatus) return; // If task not found or status didn't change, do nothing

        setTasks(prev => prev.map(t => t.id === taskId ? { ...t, status: newStatus } : t)); // Optimistically updates the task's status in the UI before the API call, makes the UI feel more responsive

        try {
            await api.put(`/tasks/${taskId}`, { status: newStatus }); // Sends API request to update the task's status in backend.
        } catch (err: any) {
            fetchTasks(); // If API call fails, refetch tasks to revert the optimistic update and show the correct status
            if (err.response?.status === 403) {
                showToast("You are not allowed to move this task"); // If the API returns a 403 error, show a specific error message about permissions
            }

        }
    };

     const handleTaskClick = (task: Task) => { // Handles clicking on a task card, opens the task details modal
        setSelectedTask(task); // Sets the selected task to show in the modal
        setShowModal(true); // Shows the modal
    };

    const handleNewTask = () => { // Handles clicking the "New Task" button, opens the task creation modal
        setSelectedTask(null); // Clears any selected task, the modal will know to show empty fields for creating a new task
        setShowModal(true); // Shows the modal
    };

     return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <div className="bg-white shadow px-8 py-4 flex justify-between items-center">
        {toast && (
            <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-6 py-3 rounded shadow-lg z-50 text-sm transition-opacity">
                {toast}
            </div>
        )}
        <h1 className="text-xl font-bold">Task Manager</h1>
        <div> 
          {/* Filters */}
            <div className="flex gap-2 mb-6">
            {(['all', 'mine', 'done'] as const).map(f => (
                <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded text-sm font-medium ${
                    filter === f
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-600 hover:bg-gray-50 border'
                }`}
                >
                {f === 'all' ? 'All Tasks' : f === 'mine' ? 'My Tasks' : 'Done'}
                </button>
            ))}
            </div>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-gray-600 text-sm">Hey, {user?.username}</span>
          <button
            onClick={handleNewTask}
            className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700"
          >
            + New Task
          </button>
          <button
            onClick={logout}
            className="bg-red-500 text-white px-4 py-2 rounded text-sm hover:bg-red-600"
          >
            Logout
          </button>
        </div>
        
      </div>

      {/* Board */}
      <div className="p-8">
        <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
          <div className="flex gap-4">
            {STATUSES.map(status => (
              <Column
                key={status}
                status={status}
                tasks={filteredTasks.filter(t => t.status === status)}
                onTaskClick={handleTaskClick}
              />
            ))}
          </div>
        </DndContext>
      </div>

      {/* Modal */}
      {showModal && (
        <TaskModal
          task={selectedTask}
          onClose={() => setShowModal(false)}
          onSaved={() => { fetchTasks(); setShowModal(false) }}
        />
      )}
    </div>
  )
}