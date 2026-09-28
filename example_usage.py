from client import ChaseLevDeque

deque = ChaseLevDeque(initial_capacity=8)
deque.push("Task-1")
deque.push("Task-2")
deque.push("Task-3")

# Thief steals from Top (FIFO)
stolen = deque.steal()
print("Thief Stole (FIFO):", stolen)

# Owner pops from Bottom (LIFO)
popped = deque.pop()
print("Owner Popped (LIFO):", popped)
