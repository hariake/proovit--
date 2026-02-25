import { useDraggable } from "@dnd-kit/core";
import { CSS } from "@dnd-kit/utilities";


// defines the shape of a task object.
export interface Task {
    id: number;
    title: string;
    description: string;
    status: string;
    deadline: string | null;
    assignee_id: number | null;
    user_id: number;
}
// TaskCard component it is draggable and shows task title, description and deadline. 
export default function TaskCard({ task, onClick }: { task: Task, onClick: (task :Task) => void }) { 
    const { attributes, listeners, setNodeRef, transform } = useDraggable({ id: task.id });

    // Applies the drag transform and transition to the card's style, making it move smoothly when dragged.
    const style = {
        transform: CSS.Translate.toString(transform),
        opacity : transform ? 0.7 : 1, // Makes the card semi-transparent while dragging
        width: "100%", // Makes the card take the full width of the column
        boxSizing: "border-box" // Ensures padding and border are included in the width, prevents layout issues when dragging
    };

   return (
  <div
    ref={setNodeRef} //sets the ref for the sortable item, necessary for drag-and-drop to work
    style={style}
    {...attributes}
    className="bg-white rounded shadow p-3 cursor-pointer hover:shadow-md transition-shadow"
  >
    <div {...listeners} className="flex flex-col gap-1">
      <p className="font-medium text-sm">{task.title}</p>
      {task.description && (
        <p className="text-xs text-gray-500 mt-1 truncate">{task.description}</p>
      )}
      {task.deadline && (
        <p className="text-xs text-red-400 mt-1">Due: {new Date(task.deadline).toLocaleDateString()}</p>
      )}
    </div>
    <button
      onClick={() => onClick(task)} // When clicking the "Edit" button, calls the onClick function passed as a prop with the task object, this will open the task details modal.
      className="text-xs text-blue-500 hover:underline mt-2"
    >
      Edit
    </button>
  </div>
   )}