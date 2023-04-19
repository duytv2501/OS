class Process:
    def __init__(self):
        self.pid = 0
        self.arrivalTime = 0
        self.burstTime = 0
        self.burstTimeRemaining = 0
        self.completionTime = 0
        self.turnaroundTime = 0
        self.waitingTime = 0
        self.isComplete = False
        self.inQueue = False


def check_for_new_arrivals(processes, n, current_time, ready_queue):
    for i in range(n):
        p = processes[i]
        # checking if any processes has arrived
        # if so, push them in the ready Queue.
        if p.arrivalTime <= current_time and not p.inQueue and not p.isComplete:
            processes[i].inQueue = True
            ready_queue.append(i)


def update_queue(processes, n, quantum, ready_queue, current_time, programs_executed):
    i = ready_queue[0]
    ready_queue.pop(0)

    # if the process is going to be finished executing,
    # ie, when it's remaining burst time is less than time quantum
    # mark it completed and increment the current time
    # and calculate its waiting time and turnaround time
    if processes[i].burstTimeRemaining <= quantum:
        processes[i].isComplete = True
        current_time += processes[i].burstTimeRemaining
        processes[i].completionTime = current_time
        processes[i].waitingTime = processes[i].completionTime - processes[i].arrivalTime - processes[i].burstTime
        processes[i].turnaroundTime = processes[i].waitingTime + processes[i].burstTime

        if processes[i].waitingTime < 0:
            processes[i].waitingTime = 0

        processes[i].burstTimeRemaining = 0

        # if all the processes are not yet inserted in the queue,
        # then check for new arrivals
        if programs_executed != n:
            check_for_new_arrivals(processes, n, current_time, ready_queue)
    else:
        # the process is not done yet. But it's going to be pre-empted
        # since one quantum is used
        # but first subtract the time the process used so far
        processes[i].burstTimeRemaining -= quantum
        current_time += quantum

        # if all the processes are not yet inserted in the queue,
        # then check for new arrivals
        if programs_executed != n:
            check_for_new_arrivals(processes, n, current_time, ready_queue)
        # insert the incomplete process back into the queue
        ready_queue.append(i)


def output(processes, n):
    avg_waiting_time = 0
    avg_turntaround_time = 0
    # sort the processes array by processes.PID
    processes.sort(key=lambda p: p.pid)

    for i in range(n):
        print("Process ", processes[i].pid, ": Waiting Time: ", processes[i].waitingTime,
              " Turnaround Time: ", processes[i].turnaroundTime, sep="")
        avg_waiting_time += processes[i].waitingTime
        avg_turntaround_time += processes[i].turnaroundTime
    print("Average Waiting Time: ", avg_waiting_time / n)
    print("Average Turnaround Time: ", avg_turntaround_time / n)


def round_robin(processes, n, quantum):
    ready_queue = []
    ready_queue.append(0)  # initially, pushing the first process which arrived first
    processes[0].inQueue = True

    current_time = 0  # holds the current time after each process has been executed
    programs_executed = 0  # holds the number of programs executed so far

    while len(ready_queue) != 0:
        update_queue(processes, n, quantum, ready_queue, current_time, programs_executed)


def main():
    n = int(input("Enter the number of processes: "))
    quantum = int(input("Enter time quantum: "))

    processes = []

    for i in range(n):
        print("Enter arrival time and burst time of each process ", i + 1, ": ", sep="", end="")
        arrival_time = int(input())
        burst_time = int(input())
        proc = Process()
        proc.arrivalTime = arrival_time
        proc.burstTime = burst_time
        proc.burstTimeRemaining = burst_time
        proc.pid = i + 1
        processes.append(proc)
        print("")

    # stl sort in terms of arrival time
    processes.sort(key=lambda p: p.arrivalTime)

    round_robin(processes, n, quantum)

    output(processes, n)
if __name__ == '__main__':
    main()