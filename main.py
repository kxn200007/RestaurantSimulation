import threading
import random
import time

# Define the number of tables, seats, waiters, and customers
num_tables = 3
num_seats = 4
num_waiters = 3
num_customers = 40

# Create semaphores for table seats and waiter calls
table_seats = [threading.Semaphore(value=num_seats) for _ in range(num_tables)]
table_locks = [threading.Lock() for _ in range(num_tables)]
waiter_called = [threading.Semaphore(value=0) for _ in range(num_tables)]

# Create locks for the kitchen, payment, and entry doors
kitchen_lock = threading.Lock()
payment_lock = threading.Lock()
entry_doors = [threading.Semaphore(value=1) for _ in range(2)]


# Initialize the finished customers counter and associated lock
finished_customers = 0
finished_customers_lock = threading.Condition()

# Define the waiter thread function
def waiter_thread(waiter_id):
    while True:
        table_id = waiter_id
        waiter_called[table_id].acquire()

        with finished_customers_lock:
            if finished_customers >= num_customers:
                break

        print(f"Waiter {waiter_id} goes to table {table_id}.")
        time.sleep(random.uniform(0.1, 0.5))

        with kitchen_lock:
            print(f"Waiter {waiter_id} delivers order to kitchen.")
            time.sleep(random.uniform(0.1, 0.5))

        time.sleep(random.uniform(0.3, 1.0))

        with kitchen_lock:
            print(f"Waiter {waiter_id} picks up order from kitchen.")
            time.sleep(random.uniform(0.1, 0.5))

        print(f"Waiter {waiter_id} serves table {table_id}.")

    with finished_customers_lock:
        finished_customers_lock.notify_all()
    print(f"Waiter {waiter_id} cleans table {table_id} and leaves the restaurant.")


# Define the customer thread function
def customer_thread(customer_id):
    choice = random.randint(0, num_tables - 1)
    backup_choice = random.randint(0, num_tables - 1) if random.random() < 0.5 else None

    door = random.choice(entry_doors)
    door.acquire()
    time.sleep(0.1)
    door.release()

    table_id = choice
    if backup_choice is not None and table_locks[choice].locked():
        table_id = backup_choice

    with table_locks[table_id]:
        table_seats[table_id].acquire()
        print(f"Customer {customer_id} sits at table {table_id}.")
        waiter_called[table_id].release()

        time.sleep(random.uniform(0.2, 1.0))
        table_seats[table_id].release()
        print(f"Customer {customer_id} leaves table {table_id}.")

    with payment_lock:
        print(f"Customer {customer_id} pays.")
    print(f"Customer {customer_id} leaves the restaurant.")

    with finished_customers_lock:
        global finished_customers
        finished_customers += 1
        if finished_customers == num_customers:
            for _ in range(num_waiters):
                waiter_called[table_id].release()
            finished_customers_lock.notify_all()

# Create waiter and customer threads
waiter_threads = [threading.Thread(target=waiter_thread, args=(i,)) for i in range(num_waiters)]
customer_threads = [threading.Thread(target=customer_thread, args=(i,)) for i in range(num_customers)]

for waiter in waiter_threads:
    waiter.start()
for customer in customer_threads:
    customer.start()

for waiter in waiter_threads:
    waiter.join()
for customer in customer_threads:
    customer.join()

print("Finished")