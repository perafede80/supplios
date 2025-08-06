from engine import Workflow, Task, Link, ConditionalLink, WorkflowEngine
from constants import Status

def setup_new_engine():
    """
    A helper function to create a fresh instance of the workflow engine
    with all tasks and links defined. This ensures each simulation is independent.
    """
    # --- Create Components ---
    flight_booking_workflow = Workflow(name='Flight Booking')
    search_flight = Task(name='Search Flights')
    select_flight = Task(name='Select Flight')
    choose_authentication = Task(name='Choose Authentication')
    passenger_detail = Task(name='Enter Passenger Details')
    add_extras = Task(name='Add Extras')
    process_payment = Task(name='Process Payment')
    finalize_booking = Task(name='Finalize Booking')

    # --- Create and Configure Engine ---
    engine = WorkflowEngine(workflow=flight_booking_workflow)
    tasks = [search_flight, select_flight, choose_authentication, passenger_detail, add_extras, process_payment, finalize_booking]
    for task in tasks:
        engine.add_task(task)

    # --- Define Links ---
    engine.add_link(Link(flight_booking_workflow, Status.IN_PROGRESS, search_flight, Status.IN_PROGRESS))
    engine.add_link(Link(search_flight, Status.COMPLETED, select_flight, Status.IN_PROGRESS))
    engine.add_link(Link(select_flight, Status.COMPLETED, choose_authentication, Status.IN_PROGRESS))

    engine.add_link(Link(choose_authentication, Status.GUEST_USER, passenger_detail, Status.IN_PROGRESS))
    engine.add_link(Link(choose_authentication, Status.GUEST_USER, add_extras, Status.IN_PROGRESS))
    engine.add_link(Link(choose_authentication, Status.REGISTERED_USER, passenger_detail, Status.IN_PROGRESS))
    engine.add_link(Link(choose_authentication, Status.REGISTERED_USER, add_extras, Status.IN_PROGRESS))

    engine.add_link(ConditionalLink(
        sources=[passenger_detail, add_extras],
        required_state=Status.COMPLETED,
        target=process_payment,
        target_state=Status.IN_PROGRESS
    ))

    engine.add_link(Link(process_payment, Status.SUCCESSFUL, finalize_booking, Status.SUCCESSFUL))
    engine.add_link(Link(process_payment, Status.FAILED, finalize_booking, Status.FAILED))

    engine.add_link(Link(finalize_booking, Status.SUCCESSFUL, flight_booking_workflow, Status.COMPLETED))
    engine.add_link(Link(finalize_booking, Status.FAILED, flight_booking_workflow, Status.FAILED))

    return engine, {
        "workflow": flight_booking_workflow,
        "search": search_flight,
        "select": select_flight,
        "auth": choose_authentication,
        "details": passenger_detail,
        "extras": add_extras,
        "payment": process_payment,
        "finalize": finalize_booking
    }

def simulate(user_type, payment_outcome):
    """
    Runs a complete workflow simulation with parameterized user type and payment status.
    :param user_type: The type of user for the simulation.
    :param payment_outcome: The desired outcome of the payment.
    """
    header = f"SIMULATION: {payment_outcome} Booking as {user_type}"
    print("\n" + "="*len(header))
    print(f"  {header}")
    print("="*len(header) + "\n")
    engine, components = setup_new_engine()

    print("\nStep 1: User starts the booking process.")
    engine.update_component_state(components["workflow"], Status.IN_PROGRESS)
    print("\n")

    print("Step 2: User completes the 'Search Flight' task.")
    engine.update_component_state(components["search"], Status.COMPLETED)
    print("\n")

    print("Step 3: User completes the 'Select Flight' task.")
    engine.update_component_state(components["select"], Status.COMPLETED)
    print("\n")

    print(f"Step 4: User chooses to continue as a {user_type}.")
    engine.update_component_state(components["auth"], user_type)
    print("\n")

    print("Step 5: User completes the 'Enter Passenger Details' task.")
    engine.update_component_state(components["details"], Status.COMPLETED)
    print("\n")

    print("Step 6: User completes the 'Add Extras' task.")
    engine.update_component_state(components["extras"], Status.COMPLETED)
    print("\n")

    print(f"Step 7: User's payment is {payment_outcome}.")
    engine.update_component_state(components["payment"], payment_outcome)
    print("\n")

    print("\n--- FINAL STATE ---")
    print(f"Final Workflow State: {engine.workflow.state.value}\n")
