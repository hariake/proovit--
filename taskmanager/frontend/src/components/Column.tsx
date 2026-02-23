import { useDroppable } from "@dnd-kit/core";
import TaskCard, { type Task } from "./TaskCard";

const LABELS: Record<string, string> = { //gives labels for the column statuses according to the backend task statuses.
    "todo": "To Do",
    "being_done": "In Progress",
    "done": "Done"
}

const COLORS: Record<string, string> = { //gives colors for the column statuses according to the backend task statuses.
    "todo": "bg-blue-500",
    "being_done": "bg-yellow-500",
    "done": "bg-green-500"
}

export default function Column({ status, tasks, onTaskClick }: { 
    status: string;
    tasks: Task[];
    onTaskClick: (task: Task) => void;
}) {
    const { setNodeRef } = useDroppable({ id: status }); // Sets up the column as a droppable area for drag-and-drop, using the status as the droppable ID

    return (
    <div className="flex-1 min-w-[250px]">
      <div className={`${COLORS[status]} rounded-t px-3 py-2 font-semibold text-sm`}> 
        {LABELS[status]} ({tasks.length})
      </div>
      <div
        ref={setNodeRef}
        className="bg-gray-50 rounded-b p-2 min-h-[400px] flex flex-col gap-2">
          {tasks.map(task => (
            <TaskCard key={task.id} task={task} onClick={onTaskClick} />
          ))}
      </div>
    </div>
  )
}
