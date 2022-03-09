#!/usr/bin/env python
"""
Downlaods and test the model marked for production
"""
import argparse
import logging
import wandb
import pandas as pd

import mlflow
from sklearn.metrics import mean_absolute_error


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="test_artifacts")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.test_data).file()
    test_data = pd.read_csv(artifact_local_path)

    X_test = test_data
    y_test = X_test.pop('price')

    model_export_path = run.use_artifact(args.model_artifact).download()
    pipe = mlflow.sklearn.load_model(model_export_path)

    y_pred = pipe.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)

    logger.info(f"Test MAE: {mae}")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Tests the regression model")


    parser.add_argument(
        "--model_artifact", 
        type=str,
        help="Model artifact required to infer on test data",
        required=True
    )

    parser.add_argument(
        "--test_data", 
        type=str,
        help="Name of the test file to download",
        required=True
    )


    args = parser.parse_args()

    go(args)
