import click

from app.deployment_manager import DeploymentManager


@click.command()
@click.argument(
    "application_name",  # Step 1 : get application name parameter
    type=str,
    required=True,
)
def sync_cmd(application_name: str) -> None:
    deployment_manager = DeploymentManager(application_name=application_name)
    deployment_manager.sync()


if __name__ == "__main__":
    sync_cmd()
