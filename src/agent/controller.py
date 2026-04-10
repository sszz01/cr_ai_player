from .types import AgentAction


class DryRunController:
    """Controller stub: logs chosen actions without clicking."""

    def execute(self, action: AgentAction) -> None:
        print(f"ACTION: {action.kind:>6} | lane={action.lane:<6} | reason={action.reason}")

