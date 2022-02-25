#!/usr/bin/env python
"""
downloads data from URL and saves as input artifact to wandb
"""
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="download_data")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info("Downloading the input artifact")
    file_path = run.use_artifact(args.sample).file()

    artifact = wandb.Artifact(name=args.artifact_name,
                                type=args.artifact_type,
                                description=args.description)

    artifact.add_file(file_path)
    logger.info("Uploading input file as artifact to wandb")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Downloads Data from URL")


    parser.add_argument(
        "--sample", 
        type=str,
        help="URL to donwload the input artifact",
        required=True
    )

    parser.add_argument(
        "-- artifact_name", 
        type=str,
        help="Name of the artifact",
        required=True
    )

    parser.add_argument(
        "-- artifact_type", 
        type=str,
        help="Type of the artifact",
        required=True
    )

    parser.add_argument(
        "-- artifact_description", 
        type=str,
        help="Description of the artifact",
        required=True
    )


    args = parser.parse_args()

    go(args)
