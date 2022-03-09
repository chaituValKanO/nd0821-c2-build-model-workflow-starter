#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)
    
    local_path = run.use_artifact(args.input_artifact).file()
    logger.info(f"Downloaded the input artifact to {local_path}")

    df = pd.read_csv(local_path)

    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price

    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(name=args.output_artifact,
                    type=args.output_type,
                    description=args.output_description)
    
    artifact.add_file("clean_sample.csv")
    logger.info("Uploading the cleaned artifact to wandb")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price of the room",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price of the room",
        required=True
    )

    args = parser.parse_args()

    go(args)
