from typing import List
from survey_parser_plugins.core import SurveyParser
import pandas as pd
import pickle
from prv_detection_step.core.strategy.base_strategy import BasePrvCandidatesStrategy

# Keys used on non detections for ZTF
NON_DET_KEYS = ["mjd", "diffmaglim", "fid"]


# Implementation a new parser for PreviousCandidates with SurveyParser signs.
class ZTFPreviousCandidatesParser(SurveyParser):
    _source = "ZTF"
    _celestial_errors = {
        1: 0.065,
        2: 0.085,
        3: 0.01,
    }
    _generic_alert_message_key_mapping = {
        "candid": "candid",
        "mjd": "jd",
        "fid": "fid",
        "pid": "pid",
        "ra": "ra",
        "dec": "dec",
        "mag": "magpsf",
        "e_mag": "sigmapsf",
        "isdiffpos": "isdiffpos",
        "rb": "rb",
        "rbversion": "rbversion",
    }

    @classmethod
    def parse_message(cls, message: dict) -> dict:
        if not cls.can_parse(message):
            raise KeyError("This parser can't parse message")
        prv_content = cls._generic_alert_message(
            message, cls._generic_alert_message_key_mapping
        )
        # attributes modification
        prv_content["mjd"] = prv_content["mjd"] - 2400000.5
        prv_content["isdiffpos"] = 1 if prv_content["isdiffpos"] in ["t", "1"] else -1
        e_radec = cls._celestial_errors[prv_content["fid"]]
        prv_content["e_ra"] = (
            prv_content["sigmara"] if "sigmara" in prv_content else e_radec
        )
        prv_content["e_dec"] = (
            prv_content["sigmadec"] if "sigmadec" in prv_content else e_radec
        )
        return prv_content

    @classmethod
    def can_parse(cls, message: dict) -> bool:
        return True

    @classmethod
    def parse(cls, messages: List[dict]) -> List[dict]:
        return list(map(cls.parse_message, messages))


class ZTFPrvCandidatesStrategy(BasePrvCandidatesStrategy):
    def process_prv_candidates(self, alerts: pd.DataFrame):
        prv_objects = []
        for index, alert in alerts.iterrows():
            prv_object = {}
            prv_object["new_alert"] = alert.to_dict()
            detections = []
            non_detections = []
            candid = alert["candid"]
            if alert["extra_fields"]["prv_candidates"] is not None:
                prv_candidates = pickle.loads(alert["extra_fields"]["prv_candidates"])
                for prv in prv_candidates:
                    if prv["candid"] is None:
                        non_detections.append(prv)
                    else:
                        detections.append(prv)
                del alert["extra_fields"]["prv_candidates"]
                detections = ZTFPreviousCandidatesParser.parse(detections) # no se parsean nunca
                non_detections = (
                    pd.DataFrame(non_detections)
                    if len(non_detections)
                    else pd.DataFrame(columns=NON_DET_KEYS)
                )

                if len(non_detections):
                    non_detections["mjd"] = non_detections["jd"] - 2400000.5
                    non_detections = non_detections[NON_DET_KEYS]
                prv_object["prv_detections"] = detections
                prv_object["non_detections"] = non_detections.to_dict('records')
            prv_objects.append(prv_object)
        return pd.DataFrame(prv_objects)
