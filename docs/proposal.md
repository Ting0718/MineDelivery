---
layout: default
title:  Proposal
---

## Summary of the Project
Our project will simulate a city where many customers continuously order food delivery from a restaurant. Customers will make their orders with certain probability distribution during one day. Input is the number of delivery men, locations of all customers, and time-based distributions of their orders during one day. Our goal is to deliver foods to all customers within shortest cumulative waiting time in one day.

## AI/ML Algorithms
We will use reinforcement learning, Q-learning, and greedy-algorithm to complete our project.

## Evaluation Plan
Quantitative: The baseline of our project is to assign each food order to the nearest delivery man and complete all the food delivery orders. We are using several metrics to evaluate our performance:
1. The cumulative waiting time of all the customers. We will try to minimize the total waiting time of all the customers because if a customer has to wait for a long time for his or her order to come, the satisfaction rate of the customers will be very low.
2. The number of orders that are not delivered withing one hour. We need to make sure that the waiting time of each customer will not exceed the resonable range.

Qualitative: It will be impressive if there is no another arrangement that would minimize the total waiting time and there is no customers waiting more than an hour. 

## Appointment with the Instructor
Oct. 21 10:10AM, 2019
