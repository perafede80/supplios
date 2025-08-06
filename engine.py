from constants import Status

class StatefulComponent:
    """A base class for any component that has a name and manages its own state."""
    def __init__(self, name, initial_state=Status.NOT_STARTED):
        self.name = name
        self.state = initial_state
        print(f"'{self.name}' created with initial state: {self.state}")

    def update_state(self, new_state: Status):
        """Updates the component's state and prints the change."""
        print(f"--> STATE CHANGE: '{self.name}' is moving from '{self.state}' to '{new_state}'")
        self.state = new_state

    def __repr__(self):
        """Provides a representation of the object."""
        return f"{type(self).__name__}(name='{self.name}', state='{self.state}')"


class Workflow(StatefulComponent):
    """Represents the overall process engine, inheriting state management."""
    pass


class Task(StatefulComponent):
    """Represents a subcomponents of a workflow, inheriting state management."""
    pass


class Link:
    """Define the relationships between a source component and a target component."""
    # TODO: think about how to manage it with an eventual user type or a payment outcome
    def __init__(self, source: StatefulComponent, source_state: Status, target: StatefulComponent, target_state: Status):
        self.source = source
        self.source_state = source_state
        self.target = target
        self.target_state = target_state

    def __repr__(self):
        return f"Link(When '{self.source.name}' is '{self.source_state.value}', set '{self.target.name}' to '{self.target_state.value}')"


class ConditionalLink:
    """
    Defines a rule where one or many source component(s) must be in a specific
    state (merge point) to trigger a state change in a target component.
    """
    # TODO: think about how to manage it with an eventual user type or a payment outcome
    def __init__(self, sources: list[StatefulComponent], required_state: Status, target: StatefulComponent, target_state: Status):
        self.sources = sources
        self.required_state = required_state
        self.target = target
        self.target_state = target_state

    def check_condition(self) -> bool:
        """Returns True only if all source components are in the required state."""
        return all(s.state == self.required_state for s in self.sources)

    def __repr__(self):
        """Provides a representation of the object"""
        source_names = [s.name for s in self.sources]
        return f"ConditionalLink(When {source_names} are all '{self.required_state.value}', set '{self.target.name}' to '{self.target_state.value }')"

class WorkflowEngine:
    def __init__(self, workflow):
        self.workflow = workflow
        self.tasks = []
        self.links = []

    def add_task(self, task):
        self.tasks.append(task)

    def add_link(self, link):
        self.links.append(link)

    def update_component_state(self, component_to_update: StatefulComponent, new_state: Status):
        if not component_to_update:
            print("Error: A valid component was not provided.")
            return

        component_to_update.update_state(new_state)
        self._process_links(component_to_update)

    def _process_links(self, changed_component):
        print("--- Checking links for cascades ---")
        # Iterate through all links to find cascades
        for link in self.links:
            if isinstance(link, Link):
                # Handle simple links
                if link.source == changed_component and link.source.state == link.source_state:
                    link.target.update_state(link.target_state)
                    # Recursively check for further cascades
                    self._process_links(link.target)
            elif isinstance(link, ConditionalLink):
                # Handle conditional links
                if changed_component in link.sources and link.check_condition():
                    link.target.update_state(link.target_state)
                    self._process_links(link.target)