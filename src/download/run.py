#!/usr/bin/env python
"""
downloads data from URL and saves as input artifact to wandb
"""
import os
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="download_data")
    run.config.update(args)

    artifact = wandb.Artifact(name=args.artifact_name,
                                type=args.artifact_type,
                                description=args.artifact_description)

    artifact.add_file(os.path.join("data", args.sample))
    logger.info(f"Uploading {args.artifact_name} as artifact to wandb")
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
        "--artifact_name", 
        type=str,
        help="Name of the artifact",
        required=True
    )

    parser.add_argument(
        "--artifact_type", 
        type=str,
        help="Type of the artifact",
        required=True
    )

    parser.add_argument(
        "--artifact_description", 
        type=str,
        help="Description of the artifact",
        required=True
    )


    args = parser.parse_args()

    go(args)
