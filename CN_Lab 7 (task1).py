import numpy as np

class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.customers = []

    def add_customer(self, customer):
        if len(self.customers) < self.capacity:
            self.customers.append(customer)
        else:
            return False
        return True

    def remove_customer(self):
        if self.customers:
            return self.customers.pop(0)
        return None

def simulate_alternative_routing(arrival_rates_Q1, blocking_probs_Q1, arrival_rates_Q3, num_iterations=1000):
    num_queues = 3
    queues = [Queue(5) for _ in range(num_queues)]
    mean_customers = [[] for _ in range(num_queues)]

    for _ in range(num_iterations):
        for i, queue in enumerate(queues):
            if i == 0:  # Queue Q1
                blocking_prob = np.random.choice(blocking_probs_Q1)
                if np.random.rand() < arrival_rates_Q1:
                    customer = 1
                    if not queue.add_customer(customer):
                        if len(queues[1].customers) < 3:
                            queues[1].add_customer(customer)
                        else:
                            queues[2].add_customer(customer)
            elif i == 1:  # Queue Q2
                if len(queues[i].customers) < queues[i].capacity:
                    if queues[0].customers:
                        customer = queues[0].remove_customer()
                        queues[i].add_customer(customer)
            else:  # Queue Q3
                if np.random.rand() < arrival_rates_Q3:
                    customer = 1
                    if len(queues[i].customers) < queues[i].capacity:
                        queues[i].add_customer(customer)

        for i, queue in enumerate(queues):
            mean_customers[i].append(len(queue.customers))

    mean_customers = [sum(queue) / len(queue) for queue in mean_customers]
    return mean_customers

# Example usage
arrival_rates_Q1 = [0.5, 0.7, 0.9]  # Example arrival rates for Q1
blocking_probs_Q1 = [0.1, 0.2, 0.3]   # Example blocking probabilities for Q1
arrival_rates_Q3 = [0.6, 0.7, 0.9]   # Example arrival rates for Q3

mean_customers = simulate_alternative_routing(arrival_rates_Q1, blocking_probs_Q1, arrival_rates_Q3)
print("Mean Customers in Q1, Q2, Q3:", mean_customers)
