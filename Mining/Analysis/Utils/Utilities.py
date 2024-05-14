import re


class Utility:
    """
    A class that contains utility methods.
    """

    @staticmethod
    def find_pattern(text, pattern):
        """
        Returns the lines where a specific pattern is found in the text.

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
        Parameters that will be pass to the method are:
            - commit_short_hash: The short hash of the commit.
            - smells_abbreviation: The abbreviation of the smells.
            - line_number: The line number of the smells.
        """
        return f"{commit_short_hash}{smells_abbreviation}L{line_number}"
