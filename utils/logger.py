import logging
import os
from datetime import datetime


def setup_logger():

    os.makedirs("output/logs", exist_ok=True)

    logfile = os.path.join(
        "output/logs",
        f"MarketIntel_{datetime.now():%Y%m%d}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(logfile, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("MarketIntel")