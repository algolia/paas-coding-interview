# paas-coding-interview

## Study case

This exercise is about building a small deployment workflow CLI.

At Algolia, applications can be deployed through ArgoCD and monitored with Datadog.
During deployments, some alerts may fire because pods restart, health checks briefly fail, or metrics temporarily degrade.
To avoid paging on-call engineers for expected deployment noise, the workflow temporarily creates a Datadog downtime while the ArgoCD sync runs.

## Instructions

Your task is to write a simple CLI in Go or Python.

The CLI must expose a `sync` command that receives:

- `application_name`

The command should perform the following workflow:

1. Ensure a Datadog downtime is active for the _the monitor_ associated with that application (note: Datadog downtime = "mute the alert")
2. Trigger an ArgoCD app sync for the application.
3. Remove the Datadog downtime.

> NOTES:
>
> - Real API calls are out of scope. You should mock Datadog and ArgoCD interactions with mocks that retrieve hard coded struct inspired on the [service documentation](#resources)
> - You should handle idempotency (what happen if the CLI fail in the middle of the run)
> - You should start by forking this repo. As the interview approaches the end you will create a pull request to share your work with us
> - We will reserve the last 5 minutes for you to ask us any questions

> The case may not be fully completed during the interview.
> We are interested in your approach, how you structure the solution and how you reason about failures, collaboration and idempotency.

## Resources

- https://docs.datadoghq.com/api/latest/downtimes/
- https://cd.apps.argoproj.io/swagger-ui
