import argparse

from utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="pass", description="deploy + datadog", epilog="Help")
    parser.add_argument("sync")  # positional argument
    parser.add_argument("--application_name")  # option that takes a value
    args = parser.parse_args()
    application_name = args.application_name
    logger.info("Starting the CLI for appname %s", application_name)
