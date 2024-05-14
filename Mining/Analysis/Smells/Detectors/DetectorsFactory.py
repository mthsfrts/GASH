from Mining.Analysis.Smells.Detectors.CodeQualityDetector import CodeQualityDetector as cq
from Mining.Analysis.Smells.Detectors.ConditionsDetector import ConditionsDetector as cond
from Mining.Analysis.Smells.Detectors.ContinuesOnErrorDetector import ContinueOnErrorDetector as coe
from Mining.Analysis.Smells.Detectors.GlobalsDetector import GlobalVariableDetector as gbls
from Mining.Analysis.Smells.Detectors.RetriesDetectors import RetryDetector as rt
from Mining.Analysis.Smells.Detectors.VulnerabilityDetector import VulnerabilityDetector as vul
from Mining.Analysis.Smells.Detectors.WorkflowDispatchDetector import WorkFlowDispatchDetector as wk


class DetectorFactory:
    @staticmethod
    def create_detector(detector_type, workflow):
        if detector_type == "CodeQuality":
            return cq(workflow)
        elif detector_type == "Conditions":
            return cond(workflow)
        elif detector_type == "ContinuesOnError":
            return coe(workflow)
        elif detector_type == "Globals":
            return gbls(workflow)
        elif detector_type == "Retries":
            return rt(workflow)
        elif detector_type == "Vulnerability":
            return vul(workflow)
        elif detector_type == "WorkflowDispatch":
            return wk(workflow)
        else:
            raise ValueError(f"Unknown detector type: {detector_type}")
