import re


class Utility:
    """
    A class that contains utility methods.
    """

    @staticmethod
    def find_pattern(text, pattern):
        """
        Find the lines where a specific pattern is found in the text.

        :param text: Content of the scripts.
        :param pattern: The regex pattern to be found.
        :return: A list of line numbers where the pattern was found.
        """
        lines = text.split("\n")
        matching_lines = [index + 1 for index, line in enumerate(lines) if re.search(pattern, line)]
        return matching_lines

    @staticmethod
    def generate_id(commit_short_hash, smells_abbreviation, line_number):
        """
        A method that generates a specific ID for a given smells, commit and line number.

             :param commit_short_hash: The short hash of the commit.
            :param smells_abbreviation: The abbreviation of the smells.
            :param line_number: The line number of the smells.

            :return: A string that represents the ID of the smells.
        """
        return f"{commit_short_hash}{smells_abbreviation}L{line_number}"

    @staticmethod
    def is_critical_branch(content, critical_branches=None):
        """
        Check if the workflow is configured for critical branches like master or main.

        :param content: The content of the workflow.
        :param critical_branches: List of critical branches to check
        against. Defaults to ["master", "main", "production"].
        :return: Boolean indicating if it's a critical branch.
        """
        if critical_branches is None:
            critical_branches = ["master", "main", "production"]

        try:
            push_branches = content.get("on", {}).get("push", {}).get("branches", [])
        except AttributeError:
            push_branches = []

        for branch in critical_branches:
            if branch in push_branches:
                return True
        return False
