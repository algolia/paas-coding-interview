import click
from paas_coding_interview import datadog_mocks, argo_mocks, errors
from paas_coding_interview.registries import registry


@click.group()
def paas():
    pass

@paas.command()
@click.argument('application_name')
def deploy(application_name: str):
    # Validate application exists in registry
    application = registry.get_application(application_name)
    
    # We don't want to deploy if the application has an existing downtime
    if application.has_datadog_downtime():
        raise errors.ApplicationIsDownError(application)
    
    # We can schedule a downtime for the application has it does not have an existing downtime
    application.schedule_datadog_downtime()
    click.echo("Datadog downtime scheduled")

    # Sync the application with Argo CD - aka deploy the application
    try:
        sync_status = application.argo_sync()
        if not sync_status.success:
            raise errors.ApplicationSyncError(application)
    finally:
        # Unset the downtime in any case
        # We assume Argo CD is self-healing
        application.unset_datadog_downtime()
        click.echo("Datadog downtime unset")
        
    click.echo(sync_status.message)

if __name__ == '__main__':
    paas()