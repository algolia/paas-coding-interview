import click
from pass_coding_interview import datadog_mocks, argo_mocks


@click.group()
def paas():
    click.echo("Hello")

@paas.command()
@click.argument('application_name')
def deploy(application_name: str):
    

    # set datadog downtime for the application
    is_down = get_downtimes(application_name)
    if is_down:
        raise ApplicationIsAlreadyDownError()
    downtime_id = schedule_downtime(application_name)
    deployed = argo_mocks.sync(application_name)
    unset_downtime(downtime_id)

    # tigger argo cd with the application name
    # unset datadog downtime

if __name__ == '__main__':
    paas()