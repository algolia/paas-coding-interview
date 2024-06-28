import json
import logging
from pathlib import Path

DEFAULT_STATE = {
    "datadog_downtime_activated": False,
    "argocd_trigger_synced": False,
    "datadog_downtime_removed": False,
}


class StateHandler:
    def __init__(self, application_name: str):
        self.application_name = application_name
        self.logger = logging.getLogger(self.__class__.__name__)
        self.state_file = Path(f"app/state/{application_name}.json")  # In-disk state
        self.state = self._init_state()  # In-memory state

    def _init_state(self):
        # Check if there is an existing file and load it into memory
        if self.state_file.exists():
            with open(self.state_file, "r", encoding="utf-8") as file:
                return json.load(file)

        # Else write one with the base state and load that base state into memory as well

        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_STATE, file)

        return DEFAULT_STATE

    def is_step_completed(self, step: str) -> bool:
        return self.state.get(step, False)

    def mark_step_completed(self, step: str):
        self.state[step] = True

        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(self.state, file)

    def reset_state(self):
        if self.state_file.exists() and self.is_step_completed("datadog_downtime_removed"):
            self.state_file.unlink()

        self.state = DEFAULT_STATE  # Reset in-memory state as well
