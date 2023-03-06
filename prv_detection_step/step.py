from apf.core.step import GenericStep

from prv_detection_step.core.candidates.process_prv_candidates import (
    process_prv_candidates,
)
from prv_detection_step.core.strategy.ztf_strategy import ZTFPrvCandidatesStrategy
from prv_detection_step.core.processor.processor import Processor

from typing import Tuple

import numpy as np
import pandas as pd
import logging


class PrvDetectionStep(GenericStep):
    """PrvDetectionStep Description

    Parameters
    ----------
    consumer : GenericConsumer
        Description of parameter `consumer`.
    **step_args : type
        Other args passed to step (DB connections, API requests, etc.)

    """

    def __init__(
        self,
        consumer=None,
        config=None,
        level=logging.INFO,
        producer=None,
        **step_args,
    ):
        super().__init__(consumer, config=config, level=level)
        self.prv_candidates_processor = Processor(
            ZTFPrvCandidatesStrategy()
        )  # initial strategy (can change)
        self.producers = {
            "scribe": producer,
            "alerts": None
        }

    def execute(self, messages):
        self.logger.info("Processing %s alerts", str(len(messages)))
        alerts = pd.DataFrame(messages)
        # If is an empiric alert must has stamp
        alerts["has_stamp"] = True
        # Process previous candidates of each alert
        prv_candidates = process_prv_candidates(self.prv_candidates_processor, alerts)
        return prv_candidates.to_dict('records')

