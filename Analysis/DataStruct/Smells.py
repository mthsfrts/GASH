class Smells:
    """
    A class to represent a smell struct.
    Parameters that will be used in the smell structure:
        - category: The category of the smell
        - name: The type of the smell
        - description: A description of the smell
        - strategy: The strategy to detect the smell
        - mitigation: The mitigation strategy for the smell
        - severity_level: The severity level of the smell
        - severity_justification: The justification for the severity level
    """

    def __init__(self, category, name, description, strategy, mitigation, severity_level, severity_justification):
        self.category = category
        self.name = name
        self.description = description
        self.strategy = strategy
        self.mitigation = mitigation
        self.severity_level = severity_level
        self.severity_justification = severity_justification

    def __str__(self):
        return (f"Category: {self.category}\n"
                f"Name: {self.name}\n"
                f"Description: {self.description}\n"
                f"Strategy: {self.strategy}\n"
                f"Mitigation: {self.mitigation}\n"
                f"Severity Level: {self.severity_level}\n"
                f"Severity Justification: {self.severity_justification}")


def create_smells_from_dict(severities):
    smells_list = []
    for category, data in severities["Categories"].items():
        for smell_name, smell_data in data["Smells"].items():
            smellier = Smells(
                category=category,
                name=smell_name,
                description=smell_data["Description"],
                strategy=smell_data["Strategy"],
                mitigation=smell_data["Mitigation"],
                severity_level=smell_data["Vulnerability"]["Level"],
                severity_justification=smell_data["Vulnerability"]["Justification"]
            )
            smells_list.append(smellier)
    return smells_list

# Dictionaries and lists of variables and params for the smells
PROMPTS = {
    "conditions": "Analyze the following condition for potential issues:\n\n",
    "vulnerabilities": "Analyze the following content for potential vulnerabilities:\n\n",
    "workflow_dispatch": "Analyze the following workflow dispatch for potential issues:\n\n",
    "global_variables": "Analyze the following global variable for potential issues:\n\n"
}

SEVERITIES = {
    "Categories": {
        "Security": {
            "Smells": {
                "HardCodedSecrets": {
                    "Strategy": "Check for the presence of secrets directly in the YAML files.",
                    "Description": "Secrets and credentials stored directly in the code, exposing sensitive data.",
                    "Mitigation": "Use GitHub Secrets to store sensitive information.",
                    "Vulnerability": {
                        "Level": "Critical",
                        "Justification": "Exposing credentials can lead to serious security breaches."
                    }
                },
                "InefficientUseOfFailFastAndContinueOnError": {
                    "Strategy": "Check the configuration of `fail-fast` and `continue-on-error` to ensure they are "
                                "used correctly.",
                    "Description": "Configurations that can lead to unnecessary executions or mask failures.",
                    "Mitigation": "Use `fail-fast` and `continue-on-error` appropriately to ensure efficient and "
                                  "transparent executions.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can mask issues or cause unnecessary executions, increasing debugging "
                                         "complexity."
                    }
                },
                "RetryFailure": {
                    "Strategy": "Identify automatic retries that mask real problems.",
                    "Description": "Automatic retries that can hide intermittent issues.",
                    "Mitigation": "Investigate and fix the underlying causes of failures instead of automatically "
                                  "retrying.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can mask issues affecting system reliability."
                    }
                },
                "DeprecatedOrUnsafeLibraries": {
                    "Strategy": "Check the use of outdated or known unsafe libraries.",
                    "Description": "Use of libraries that no longer receive updates or have known vulnerabilities.",
                    "Mitigation": "Keep libraries up to date and use dependency analysis tools.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can introduce known vulnerabilities into the system."
                    }
                },
                "FlakyTests": {
                    "Strategy": "Detect tests that fail intermittently.",
                    "Description": "Tests that fail randomly, causing uncertainty in results.",
                    "Mitigation": "Identify and fix the root cause of test flakiness.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Reduces confidence in test results."
                    }
                }
            }
        },
        "Maintenance": {
            "Smells": {
                "PushEventMisconfiguration": {
                    "Strategy": "Check push configurations associated with branches and tags.",
                    "Description": "Misconfiguration of push events, such as lack of filters for specific branches or "
                                   "tags.",
                    "Mitigation": "Use appropriate filters for branches and tags.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can lead to unnecessary workflow executions and increase CI/CD load."
                    }
                },
                "PullRequestEventMisconfiguration": {
                    "Strategy": "Check pull request configurations associated with specific branches.",
                    "Description": "Misconfiguration of pull request events, such as lack of filters for specific "
                                   "branches or merge conditions.",
                    "Mitigation": "Use appropriate filters for branches and merge conditions.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can lead to unnecessary workflow executions and potential merge conflicts."
                    }
                },
                "ReleaseEventMisconfiguration": {
                    "Strategy": "Check release configurations associated with specific versions.",
                    "Description": "Misconfiguration of release events, such as lack of filters for specific versions "
                                   "or prereleases.",
                    "Mitigation": "Use appropriate filters for versions and prereleases.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can lead to unnecessary workflow executions and incorrect version releases."
                    }
                },
                "WorkflowDispatchMisconfiguration": {
                    "Strategy": "Check the configuration of inputs in manual dispatch events.",
                    "Description": "Misconfiguration of inputs provided manually in dispatch events.",
                    "Mitigation": "Clearly validate and document the inputs needed for manual dispatch.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Incorrect inputs can lead to improper workflow execution and failures."
                    }
                },
                "WorkflowCallMisconfiguration": {
                    "Strategy": "Check the configuration of calls to other workflows.",
                    "Description": "Misconfiguration of remote workflow calls, such as lack of parameter validation.",
                    "Mitigation": "Clearly validate and document the parameters passed in workflow calls.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Incorrect calls can lead to execution failures and unresolved dependencies."
                    }
                },
                "RunEventMisconfiguration": {
                    "Strategy": "Check the configuration of run events based on the status of other workflows.",
                    "Description": "Misconfiguration of run events, such as incorrect dependencies or execution "
                                   "status settings.",
                    "Mitigation": "Properly configure dependencies and execution status.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Incorrect dependencies can lead to unnecessary executions or execution "
                                         "failures."
                    }
                },
                "FuzzyVersion": {
                    "Strategy": "Detect imprecise or missing versions in dependencies.",
                    "Description": "Use of non-specific versions for dependencies, making builds hard to reproduce.",
                    "Mitigation": "Specify exact versions for all dependencies.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can lead to inconsistencies and maintenance difficulties."
                    }
                },
                "UntrackedArtifacts": {
                    "Strategy": "Check if artifacts are generated without version control.",
                    "Description": "Generated artifacts that are not tracked or versioned, making reproduction "
                                   "difficult.",
                    "Mitigation": "Implement version control for all artifacts.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Makes build environment reproduction and maintenance difficult."
                    }
                },
                "InefficientCacheManagement": {
                    "Strategy": "Check the correct use and invalidation of caches.",
                    "Description": "Poorly managed cache that is not reused or grows unnecessarily.",
                    "Mitigation": "Properly configure cache keys and clean caches regularly.",
                    "Vulnerability": {
                        "Level": "Low",
                        "Justification": "Impacts efficiency but does not directly compromise security or "
                                         "functionality."
                    }
                },
                "InadequateLogging": {
                    "Strategy": "Check logs for sensitive data or excessive information.",
                    "Description": "Logs that expose sensitive data or are overly verbose.",
                    "Mitigation": "Use `::add-mask::` to mask sensitive data and adopt standard logging practices.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can expose sensitive data and make debugging difficult."
                    }
                },
                "ComplexEventTriggers": {
                    "Strategy": "Check the use of multiple triggers and the complexity of event configurations.",
                    "Description": "Complex event configurations that can cause undesired or unnecessary executions.",
                    "Mitigation": "Simplify event configurations and clearly document trigger logic.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Increases complexity and can lead to unexpected executions."
                    }
                },
                "ImproperUseOfMatrixStrategy": {
                    "Strategy": "Check matrix configuration for unnecessary or excessive variations.",
                    "Description": "Matrix configurations that create redundant or unnecessary job variations.",
                    "Mitigation": "Optimize matrix configuration to avoid redundant executions.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Increases execution time and resource usage."
                    }
                },
                "ConvolutedConditions": {
                    "Strategy": "Check the use of complex conditions (`if`, `with`, `needs`, etc.) that can be "
                                "simplified.",
                    "Description": "Use of complex conditions that can make the workflow hard to read and maintain.",
                    "Mitigation": "Simplify conditions and clearly document conditional logic.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Increases complexity and can introduce hard-to-debug errors."
                    }
                },
                "MisuseOfExecutionStatusChecks": {
                    "Strategy": "Check the correct use of execution status checks (`always`, `canceled`, `success`).",
                    "Description": "Improper use of execution status checks that can cause undesired executions or "
                                   "ignore failures.",
                    "Mitigation": "Properly configure status checks to ensure appropriate executions.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Can lead to undesired executions or mask important failures."
                    }
                },
                "BashScriptComplexity": {
                    "Strategy": "Check for long and complex bash scripts within steps.",
                    "Description": "Complex bash scripts that can be difficult to maintain and debug.",
                    "Mitigation": "Break complex scripts into smaller, manageable parts and add explanatory comments.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Increases maintenance difficulty and the possibility of errors."
                    }
                }
            }
        },
        "Efficiency": {
            "Smells": {
                "LongBuildTimes": {
                    "Strategy": "Monitor build execution times and identify steps causing delays.",
                    "Description": "Builds that take a long time, impacting productivity.",
                    "Mitigation": "Optimize build steps and use caching effectively.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Impacts productivity but does not directly compromise security or "
                                         "functionality."
                    }
                },
                "ExcessivePrivileges": {
                    "Strategy": "Check permissions configured in workflows.",
                    "Description": "Excessive permissions configured in workflows that can lead to security risks.",
                    "Mitigation": "Restrict permissions to the minimum necessary.",
                    "Vulnerability": {
                        "Level": "Critical",
                        "Justification": "Excessive permissions can lead to serious security compromises."
                    }
                }
            }
        },
        "Quality": {
            "Smells": {
                "TyposAndGenericWords": {
                    "Strategy": "Check job, step, and variable names for common typos or overly generic terms.",
                    "Description": "Typos and generic words that make the code hard to understand.",
                    "Mitigation": "Adopt clear naming conventions and regularly review the code.",
                    "Vulnerability": {
                        "Level": "Low",
                        "Justification": "Impacts readability and maintenance but does not directly compromise "
                                         "security or functionality."
                    }
                },
                "InconsistentNamingConventions": {
                    "Strategy": "Check if job, step, and variable names follow consistent conventions.",
                    "Description": "Inconsistent naming conventions that make the code hard to read and maintain.",
                    "Mitigation": "Adopt and follow clear naming conventions.",
                    "Vulnerability": {
                        "Level": "Low",
                        "Justification": "Impacts readability and maintenance but does not directly compromise "
                                         "security or functionality."
                    }
                },
                "LargeCodeBlocks": {
                    "Strategy": "Identify steps that contain long and complex scripts.",
                    "Description": "Large code blocks that make the code hard to read and maintain.",
                    "Mitigation": "Break long scripts into smaller, manageable parts.",
                    "Vulnerability": {
                        "Level": "Medium",
                        "Justification": "Impacts readability and maintenance, potentially leading to errors and "
                                         "debugging difficulties."
                    }
                },
                "LackOfCommentsAndDocumentation": {
                    "Strategy": "Check for the presence of explanatory comments and adequate documentation.",
                    "Description": "Lack of comments and documentation in workflows.",
                    "Mitigation": "Add explanatory comments and keep documentation up to date.",
                    "Vulnerability": {
                        "Level": "Low",
                        "Justification": "Impacts readability and maintenance but does not directly compromise "
                                         "security or functionality."
                    }
                }
            }
        }
    }
}

GENERIC_NAMES = ["generated",
                 "info",
                 "value",
                 "var",
                 "item",
                 "array",
                 "list",
                 "object"]

KEYWORDS = [
    "creds?",
    "tokens?",
    "\w*secret\w*?",
    "\w*login\w*",
    "\w*secure\w*",
    "o?auth0?",
    "\w*key\w*",
    "\w*password\w*",
    "pwd?",
    "pass(wd|phrase)?",
    "\w*registry\w*",
    "ssh_connect",
    "encryption",
    "api_key",
    "secret_key",
    "private_key",
    "access_key",
    "auth_key",
    "credential",
    "signature",
    "signing_key",
    "admin",
    "root",
    "sudo",
    "\w*token\w*",
    "db_password",
    "database_url",
    "connection_string",
    "\w*cert\w*",
    "\w*rsa\w*",
    "\w*dsa\w*",
    "\w*ecdsa\w*",
    "\w*pgp\w*",
    "\w*ssh\w*",
    "\w*ssl\w*",
    "database",
    "db_user",
    "db_name",
    "host",
    "port",
    "aws",
    "s3",
    "azure",
    "gcp",
    "salt",
    "iv",
    "cipher"
]
