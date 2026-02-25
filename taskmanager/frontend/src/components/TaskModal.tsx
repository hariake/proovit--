import { useState, useEffect } from "react";
import { type Task} from "./TaskCard";
import api from "../api/client";

// Interfaces for the user and comment objects, defines the structure of the data. 

interface User {
    id: number;
    username: string;
}

interface Comment {
    id: number;
    body: string;
    username: string;
    created_at: string;
}

export default function TaskModal({ task, onClose, onSaved }: {
    task: Task | null; // The task to show in the modal, if null, the modal will show empty fields for creating a new task
    onClose: () => void; // Function to call when the modal should be closed
    onSaved: () => void; // Function to call after a task is saved, used to refresh the task list in the dashboard
}) {
    const [title, setTitle]             = useState(""); // State for the task title input field
    const [description, setDescription] = useState(""); // State for the task description input field
    const [status, setStatus]           = useState("todo"); // State for the task status select field, defaults to "todo"
    const [deadline, setDeadline]       = useState(task?.deadline?.slice(0, 10) || ""); // State for the task deadline input field, if task has a deadline, initialize with it (formatted as YYYY-MM-DD), otherwise empty
    const [error, setError]             = useState(""); // State for any error messages to show in the modal
    const [users, setUsers]             = useState<User[]>([]); // State for the list of users to show in the assignee dropdown
    const [assigneeId, setAssigneeId]   = useState<number | null>(null); // State for the selected assignee ID in the dropdown
    const [comments, setComments]       = useState<Comment[]>([]); // State for the list of comments on the task
    const [newComment, setNewComment]   = useState(""); // State for the new comment input field

    const isEditing = !!task; // Whether we are editing an existing task or creating a new one, used to determine whether to call create or update API endpoint

        useEffect(() => { // Fetches the list of users from the backend when the modal is opened, to populate the assignee dropdown 
         api.get("/users").then(res => setUsers(res.data.users))
        }, []); // eslint-disable-line react-hooks/exhaustive-deps
    
    useEffect(() => { // When the task prop changes (e.g., when opening the modal for editing), update the form fields with the task's data
        if (task) {
            setTitle(task.title);
            setDescription(task.description);
            setStatus(task.status);
            setDeadline(task.deadline?.slice(0, 10) || "");
            setAssigneeId(task.assignee_id);
            // Fetch comments for the task
            api.get(`/tasks/${task.id}/comments`).then(res => {
                setComments(res.data.comments);
            });
        } else {
            setTitle("");
            setDescription("");
            setStatus("todo");
            setDeadline("");
            setAssigneeId(null);
            setComments([]);
        }
    }, [task]);

    const handleSave = async () => { // Handles saving the task, either creating a new task or updating an existing one based on isEditing 
        if (!title.trim()) { setError("Title is required"); return; } // Title is required, if it's empty show error and do not proceed
        try {
            if (isEditing) {
                await api.put(`/tasks/${task.id}`, { title, description, status, deadline: deadline || null, assignee_id: assigneeId }); // If editing, send PUT request to update the task
            } else {
                await api.post("/tasks", { title, description, status, deadline: deadline || null, assignee_id: assigneeId }); // If creating new, send POST request to create the task
            }
            onSaved(); // After saving, call onSaved to refresh the task list in the dashboard
        } catch (err: any) {
            if (err.response?.status === 403) {
                setError("You are not allowed to edit this task"); // If the API returns a 403 error, show a specific error message about permissions
            } else {
                setError("Failed to save task"); // For any other errors, show a generic error message
            }
        }
    };

    const handleDelete = async () => { // Handles deleting the task, only available when editing an existing task
        if (!task) return;
        try {
            await api.delete(`/tasks/${task.id}`); // Send DELETE request to delete the task
            onSaved(); // After deleting, call onSaved to refresh the task list in the dashboard
        } catch (err: any) {
                if (err.response?.status === 403) {
                    setError("You are not allowed to delete this task"); // If the API returns a 403 error, show a specific error message about permissions
                } else {
            setError("Failed to delete task"); // If API call fails, show error message
            }
        }
    };

    const handleAddComment = async () => { // Handles adding a new comment to the task
        if (!newComment.trim() || !task) return; // Comment body is required, if it's empty or task is not defined, do not proceed
        try {
            await api.post(`/tasks/${task.id}/comments`, { content: newComment }); // Send POST request to add the comment
            const res = await api.get(`/tasks/${task.id}/comments`); // After adding the comment, fetch the updated list of comments
            setComments(res.data.comments); // After successfully adding the comment, update the comments state to show it in the UI
            setNewComment(""); // Clear the new comment input field
        } catch {
            setError("Failed to add comment"); // If API call fails, show error message
        }
    };


     return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white rounded shadow-lg w-full max-w-md p-6">
        <h2 className="text-lg font-bold mb-4">{isEditing ? 'Edit Task' : 'New Task'}</h2>
        {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

        <div className="flex flex-col gap-3">
          <input
            className="border rounded p-2 text-sm"
            placeholder="Title"
            value={title}
            onChange={e => setTitle(e.target.value)}
          />
          <textarea
            className="border rounded p-2 text-sm"
            placeholder="Description"
            rows={3}
            value={description}
            onChange={e => setDescription(e.target.value)}
          />
          <select
            className="border rounded p-2 text-sm"
            value={status}
            onChange={e => setStatus(e.target.value)}
          >
            <option value="todo">To Do</option>
            <option value="being_done">In Progress</option>
            <option value="done">Done</option>
          </select>
          <input
            className="border rounded p-2 text-sm"
            type="date"
            value={deadline}
            onChange={e => setDeadline(e.target.value)}
          />
          <select
            className="border rounded p-2 text-sm"
            value={assigneeId ?? ''}
            onChange={e => setAssigneeId(e.target.value ? Number(e.target.value) : null)}
          >
            <option value="">No assignee</option>
            {users.map(u => (
              <option key={u.id} value={u.id}>{u.username}</option>
            ))}
          </select>
        </div>

        {/* Comments section, only shown when editing an existing task */}
        {isEditing && (
            <div className="mt-6">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Comments</h3>
                <div className="flex flex-col gap-2 mb-3 max-h-40 overflow-y-auto">
                    {comments.length === 0 && 
                        <p className="text-xs text-gray-500">No comments yet</p>
                    }
                    {comments.map(c => (
                        <div key={c.id} className="bg-gray-100 rounded p-2 text-sm">
                            <span className="font-medium text-blue-600">{c.username}</span>
                            <span className="text-gray-600 text-xs ml-2">
                                {new Date(c.created_at).toLocaleString()}
                            </span>
                            <p className="text-gray-800 mt-1">{c.body}</p>
                        </div>
                    ))}
                </div>
                {/* comment input */}
                <div className="flex gap-2">
                    <input
                        className="border rounded p-2 text-sm flex-1"
                        placeholder="Add a comment..."
                        value={newComment}
                        onChange={e => setNewComment(e.target.value)}
                        onKeyDown={e => e.key === "Enter" && handleAddComment}
                    />
                    <button
                        onClick={handleAddComment}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                        Add Comment
                        </button>
                    </div>
                </div>    
        )}
        <div className="flex justify-between mt-6">
          {isEditing && (
            <button onClick={handleDelete} className="text-red-500 text-sm hover:underline">
              Delete task
            </button>
          )}
          <div className="flex gap-2 ml-auto">
            <button onClick={onClose} className="px-4 py-2 text-sm border rounded hover:bg-gray-50">
              Cancel
            </button>
            <button onClick={handleSave} className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
              {isEditing ? 'Save' : 'Create'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
