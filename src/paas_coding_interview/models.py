from dataclasses import dataclass
from typing import Optional

from paas_coding_interview import datadog_mocks
from paas_coding_interview import argo_mocks


@dataclass
class ArgoSyncStatus:
    success: bool
    message: str

@dataclass
class Downtime:
    active: bool
    downtime_id: Optional[str] = None

@dataclass
class Application:
    name: str
    namespace: str
    project: str
    sync_status: Optional[str] = None
    health_status: Optional[str] = None
    downtime: Optional[Downtime] = None

    def has_datadog_downtime(self) -> bool:
        return datadog_mocks.has_downtime(self.name)

    def schedule_datadog_downtime(self) -> Downtime:
        return datadog_mocks.schedule_downtime(self.name)

    def unset_datadog_downtime(self) -> None:
        if not self.downtime:
            raise ValueError("Downtime ID is not set")
        return datadog_mocks.unset_downtime(self.downtime)

    def argo_sync(self) -> ArgoSyncStatus:
        return ArgoSyncStatus(*argo_mocks.sync(self.name))
