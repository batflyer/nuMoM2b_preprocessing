# Copyright 2019 Alexander L. Hayes

"""
===========
__main__.py
===========

Main script for interacting with the package from the command line.

TODO
====

* Options to modify config values and write them back to file.
"""

import argparse
import logging

from . import get_config
from . import preprocess

# Argument Parser

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    "-c",
    "--config",
    type=str,
    default="phi_config.json",
    help="Set the configuration file to read from [Default:phi_config.json].",
)
PARSER.add_argument(
    "-l",
    "--logging",
    type=int,
    default=10,  # logging.DEBUG
    help="Set the verbosity of the Python logger [Default:10]. Follows Logging Levels.",
)
PARSER.add_argument(
    "-t",
    "--test",
    action="store_true",
    help="Display information for unit tests, code coverage, and formatting.",
)

# Data Section

TEST_INFO = """=============
Code Quality:
=============

Unit testing and code coverage are evaluated using ``coverage``. Linting is
performed with ``pylint`` and style is enforced with ``black``.

Installation
------------

.. code-block:: bash

    pip install coverage black pylint

Unit Tests
----------

Unit tests can be a relatively easy check for everything being in working order
or whether any assumptions are violated.

From the base of the repository:

.. code-block:: bash

    coverage run phi/unittests/tests.py
    coverage html
    open htmlcov/index.html
"""

# Arguments and Configuration Files

ARGS = PARSER.parse_args()
PARAMETERS = get_config.parameters(config=ARGS.config)

# Initialize logging options

LOGFILE = PARAMETERS["log_file"] if PARAMETERS.get("log_file") else "debug.log"

logging.basicConfig(
    filename="{0}".format(LOGFILE),
    level=ARGS.logging,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
LOGGER = logging.getLogger(__name__)

LOGGER.info("Starting the logger.")

# Logic for Running

if ARGS.test:
    LOGGER.info("Displaying test information for user.")
    print(TEST_INFO)
    LOGGER.info("Reached bottom, shutting down logger.")
    exit(0)

LOGGER.info("Pre-processing the data.")

DATA = preprocess.run(PARAMETERS)

LOGGER.info("Completed pre-processing.")

# Drop the PublicID Column for learning/inference
LOGGER.info("Dropping `PublicID` column for learning/inference.")
DATA = DATA.drop("PublicID", axis=1)

# Convert the S and D values to NaN
DATA = DATA.replace(["D", "S"], float("nan"))

# Drop NaN rows
LOGGER.info("Dropping NaN rows.")
DATA = DATA.dropna()

# Write to csv
LOGGER.info("Writing data to `data.csv` file.")
DATA.to_csv("data.csv", index=False, na_rep="NaN")
LOGGER.info("Done writing data to `data.csv` file.")

LOGGER.info("Reached bottom, shutting down logger.")
logging.shutdown()
exit(0)
