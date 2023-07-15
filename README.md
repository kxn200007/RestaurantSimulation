# RestaurantSimulation
The "RestaurantSimulation" code simulates a restaurant scenario with multiple tables, seats, waiters, and customers using multithreading in Python.
It provides a simulation of the interaction between customers and waiters in a restaurant setting.

The code utilizes the threading module to create threads for waiters and customers. It uses semaphores and locks to manage the availability of table seats, handle waiter calls, and synchronize access to critical sections such as the kitchen, payment, and entry doors.

In the simulation, customers arrive, choose a table, and request a waiter. Waiters respond to customer calls, deliver orders to the kitchen, pick up orders, and serve the tables. Customers eventually leave the table, pay, and exit the restaurant. The simulation continues until all customers have finished their dining experience.

The code includes functions for the waiter threads and customer threads, where each thread represents a waiter or customer and simulates their behavior in the restaurant. The simulation also prints out relevant information and interactions between customers and waiters.

By running the "RestaurantSimulation" code, you can observe the dynamics and flow of a restaurant scenario with multiple customers and waiters. It showcases the coordination and synchronization aspects required in a real restaurant setting, providing insights into how different threads interact and access shared resources.
