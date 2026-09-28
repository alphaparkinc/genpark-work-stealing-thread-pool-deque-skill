# genpark-work-stealing-thread-pool-deque-skill

Agent Skill implementing the **Chase-Lev Work-Stealing Deque Algorithm** for parallel task schedulers, supporting lock-free owner LIFO operations and stealer FIFO operations.

## Architectural Overview
```mermaid
flowchart TD
    Owner["Owner Thread"] -->|Push / Pop LIFO| Bottom["Deque Bottom (Cache Warm)"]
    Stealer["Thief Worker Thread"] -->|Steal FIFO| Top["Deque Top (Oldest Tasks)"]
    Bottom & Top --> Buffer["Dynamically Resizing Circular Array Buffer"]
```
