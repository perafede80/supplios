# Supplios - Workflow Engine Challenge

This repository contains my implementation for the Supplios coding challenge. The project is a simple, extensible state machine and workflow engine written in Python.

## Project Structure

The project is organized into the following files:

-   `engine.py`: Contains the core components of the engine: `StatefulComponent`, `Workflow`, `Task`, `Link`, `ConditionalLink`, and the main `WorkflowEngine` orchestrator.
-   `constants.py`: Defines the unified `Status` Enum, which represents all possible states a component can have.
    -   *Note: This file contains a `TODO` comment discussing the architectural trade-offs of splitting this Enum into more specific types in a larger application.*
-   `run_simulations.py`: Defines the functions used to simulate four different scenarios based on the "Buy a Flight Ticket" use case (guest/registered user, successful/failed payment).
-   `test_engine.py`: Contains a `unittest` suite that verifies the core logic of simple and conditional links.
-   `main.py`: The main entry point to run all four simulations defined in `run_simulations.py`.

## Prerequisites

-   Python 3.x installed on your machine.

## Getting Started

1.  Clone the repository to your local machine.
2.  Navigate into the project directory.
3.  Run the simulations:
    ```bash
    python main.py
    ```

## Running Tests

To run the unit tests, execute the following command from the root of the project directory:
```bash
python -m unittest test_engine.py
```

## "Buy Flight Ticket" Scenario

The main demonstration models the process of buying a flight ticket. This workflow is composed of several tasks and rules:

1.  **Linear Steps:** The process starts with a sequence of tasks: `Search Flights` -> `Select Flight` -> `Choose Authentication`.
2.  **Parallel Fork:** After the user chooses their authentication method, the workflow splits into two parallel tasks that can be completed independently:
    * `Enter Passenger Details`
    * `Add Extras`
3.  **Conditional Merge Point:** The workflow will only proceed to the `Process Payment` task after **both** `Enter Passenger Details` and `Add Extras` are marked as `COMPLETED`. This is managed by a `ConditionalLink`.
4.  **Conditional Outcome:** The outcome of the `Process Payment` task (`SUCCESSFUL` or `FAILED`) determines the final state of the entire booking process.

## Future Improvements

As noted in the code, I considered several architectural patterns during this challenge. Future improvements could include:

1.  **Adding Diagrams:** Creating a Class Diagram (to visualize the code structure) and a State Diagram (to visualize the workflow behavior).
2.  **Refactoring Enums:** For a larger, production-scale application, I would further explore splitting the unified `Status` enum into more specific types (e.g., `TaskStatus`, `PaymentOutcome`) and refactoring the `Link` classes to handle them, as noted in the `TODO` comments.