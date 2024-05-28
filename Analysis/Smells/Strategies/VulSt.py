from abc import ABC, abstractmethod
import re
from Analysis.DataStruct import Smells
from Analysis.Utils.Utilities import Utility


class VulnerabilityCheckStrategy(ABC):
    @abstractmethod
    def check(self, workflow):
        pass


class DefaultVulnerabilityCheckStrategy(VulnerabilityCheckStrategy):
    def __init__(self):
        self.keywords = Smells.KEYWORDS

    def check(self, workflow):
        vulnerabilities = []
        content = workflow.raw_content
        seen_matches = set()
        lines = content.split("\n")
        is_critical = Utility.is_critical_branch(workflow.events)

        pattern = re.compile(r'(\w+):\s*(.*)')

        for i, line in enumerate(lines, start=1):
            key_value_match = pattern.search(line)
            if key_value_match:
                key, value = key_value_match.groups()
                for keyword in self.keywords:
                    if re.search(keyword, key, re.IGNORECASE):
                        if not re.search(r'\${{\s*secrets\.\w+\s*}}', value.strip()):
                            if (key, i) not in seen_matches:
                                seen_matches.add((key, i))
                                vulnerabilities.append({
                                    'keyword': keyword,
                                    'line': i,
                                    'key': key,
                                    'value': value.strip(),
                                    'is_critical': is_critical
                                })

        return vulnerabilities
