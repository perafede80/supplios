import unittest
from engine import Workflow, Task, Link, ConditionalLink, WorkflowEngine
from constants import Status

class TestWorkflowEngine(unittest.TestCase):
    # TODO: In the scenario of having different enum types, add a test case to ensure the engine correctly handles or raises an error
    def setUp(self):
        """Set up a fresh engine and components for each test."""
        self.workflow = Workflow(name="Test Workflow")
        self.task_a = Task(name="Task A")
        self.task_b = Task(name="Task B")
        self.task_c = Task(name="Task C")

        self.engine = WorkflowEngine(self.workflow)
        self.engine.add_task(self.task_a)
        self.engine.add_task(self.task_b)
        self.engine.add_task(self.task_c)

    def test_simple_link_cascade(self):
        """
        Tests if a simple A -> B link works correctly.
        """
        print("\n--- Running test: test_simple_link_cascade ---")

        # Rule
        self.engine.add_link(Link(self.task_a, Status.COMPLETED, self.task_b, Status.IN_PROGRESS))

        # Initial state check
        self.assertEqual(self.task_b.state, Status.NOT_STARTED)

        # Trigger the state change
        self.engine.update_component_state(self.task_a, Status.COMPLETED)

        # Assert that the cascade happened correctly
        self.assertEqual(self.task_b.state, Status.IN_PROGRESS)

    def test_conditional_link_cascade(self):
        """
        Tests if a conditional link correctly waits for multiple sources.
        """
        print("\n--- Running test: test_conditional_link_merge_point ---")

        # Rule
        self.engine.add_link(ConditionalLink(
            sources=[self.task_a, self.task_b],
            required_state=Status.COMPLETED,
            target=self.task_c,
            target_state=Status.IN_PROGRESS
        ))

        # Trigger the state change for task a
        self.engine.update_component_state(self.task_a, Status.COMPLETED)

        # Assert that task c has not changed state yet, because task b is not completed yet
        self.assertEqual(self.task_c.state, Status.NOT_STARTED)

        # Trigger the state change for task b
        self.engine.update_component_state(self.task_b, Status.COMPLETED)

        # Assert that the cascade has now happened correctly
        self.assertEqual(self.task_c.state, Status.IN_PROGRESS)

if __name__ == '__main__':
    unittest.main()