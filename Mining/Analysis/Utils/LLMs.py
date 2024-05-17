from concurrent.futures import ThreadPoolExecutor
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from textblob import TextBlob
from Mining.Analysis.DataStruct.Smells import PROMPTS


class LLMAnalyzer:
    def __init__(self):
        """
        Initialize the LLMAnalyzer with different model pipelines and prompts.
        """
        self.bert_pipeline = pipeline('text-classification', model='bert-base-uncased')
        self.roberta_pipeline = pipeline('text-classification', model='roberta-base')
        self.xlnet_pipeline = pipeline('text-classification', model='xlnet-base-cased')

        self.gpt2_model = AutoModelForCausalLM.from_pretrained('gpt2')
        self.gpt2_tokenizer = AutoTokenizer.from_pretrained('gpt2')

        self.prompts = PROMPTS

    def conditions(self, content):
        """
        Analyze the given content for condition-related issues using multiple models.

        :param content: The content to analyze.
        :return: A list of detected smells related to conditions.
        """
        smells = []
        pattern = r'if:'
        conditions = [line for line in content.split('\n') if pattern in line]
        for condition in conditions:
            bert_result = self.bert_pipeline(condition)
            roberta_result = self.roberta_pipeline(condition)
            xlnet_result = self.xlnet_pipeline(condition)
            gpt2_result = self.generate_gpt2_response(condition, self.prompts['conditions'])

            consensus_score = (bert_result[0]['score'] + roberta_result[0]['score'] + xlnet_result[0]['score'] +
                               extract_gpt2_score(gpt2_result)) / 4
            if bert_result[0]['label'] == 'LABEL_CONDITION':
                smells.append({
                    'condition': condition,
                    'score': consensus_score
                })
        return smells

    def vulnerabilities(self, content):
        """
        Analyze the given content for vulnerabilities using multiple models.

        :param content: The content to analyze.
        :return: A list of detected vulnerabilities.
        """
        vulnerabilities = []
        lines = content.split('\n')
        for line in lines:
            roberta_result = self.roberta_pipeline(line)
            xlnet_result = self.xlnet_pipeline(line)
            gpt2_result = self.generate_gpt2_response(line, self.prompts['vulnerabilities'])

            consensus_score = (roberta_result[0]['score'] + xlnet_result[0]['score'] +
                               extract_gpt2_score(gpt2_result)) / 3
            if roberta_result[0]['label'] == 'LABEL_VULNERABILITY':
                vulnerabilities.append({
                    'line': line,
                    'score': consensus_score
                })
        return vulnerabilities

    def workflow_dispatch(self, content):
        """
        Analyze the given content for workflow_dispatch-related issues using multiple models.

        :param content: The content to analyze.
        :return: A list of detected smells related to workflow_dispatch.
        """
        smells = []
        if 'workflow_dispatch' in content:
            bert_result = self.bert_pipeline(content)
            roberta_result = self.roberta_pipeline(content)
            xlnet_result = self.xlnet_pipeline(content)
            gpt2_result = self.generate_gpt2_response(content, self.prompts['workflow_dispatch'])

            consensus_score = (bert_result[0]['score'] + roberta_result[0]['score'] + xlnet_result[0]['score']
                               + extract_gpt2_score(gpt2_result)) / 4
            if bert_result[0]['label'] == 'LABEL_DISPATCH':
                smells.append({
                    'description': 'Workflow dispatch found',
                    'score': consensus_score
                })
        return smells

    def global_variables(self, content):
        """
        Analyze the given content for global variable-related issues using multiple models.

        :param content: The content to analyze.
        :return: A list of detected issues related to global variables.
        """
        global_vars = []
        lines = content.split('\n')
        for line in lines:
            gpt_result = self.generate_gpt2_response(line, self.prompts['global_variables'])
            xlnet_result = self.xlnet_pipeline(line)

            consensus_score = (extract_gpt2_score(gpt_result) + xlnet_result[0]['score']) / 2
            if "global variable" in gpt_result:
                global_vars.append({
                    'variable': line,
                    'score': consensus_score
                })
        return global_vars

    def generate_gpt2_response(self, text, prompt_key):
        """
        Generate a response from GPT-2 given the text and a key to the prompt.

        :param text: The text to analyze.
        :param prompt_key: The key to the prompt in the prompt dictionary.
        :return: The response generated by GPT-2.
        """
        prompt = self.prompts[prompt_key]
        input_text = f"{prompt} {text}"
        inputs = self.gpt2_tokenizer.encode(input_text, return_tensors='pt')
        outputs = self.gpt2_model.generate(inputs, max_length=250, num_return_sequences=1)
        response = self.gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    @staticmethod
    def extract_gpt2_score(gpt2_response):
        """
        Extract a relevance score from the GPT-2 response.

        :param gpt2_response: The response generated by GPT-2.
        :return: A relevance score extracted from the response.
        """
        relevance_score = 0.0

        keywords = ['global variable', 'issue', 'problem', 'warning', 'critical']
        for keyword in keywords:
            if keyword in gpt2_response.lower():
                relevance_score += 1.0

        sentiment = TextBlob(gpt2_response).sentiment
        relevance_score += sentiment.polarity * sentiment.subjectivity

        relevance_score = min(max(relevance_score, 0.0), 5.0)

        return relevance_score

    def analyze(self, content):
        """
        Analyze the given content for various issues using multiple models.

        :param content: The content to analyze.
        :return: A dictionary of analysis results.
        """
        analyses = {
            'conditions': None,
            'vulnerabilities': None,
            'workflow_dispatch': None,
            'global_variables': None
        }

        # Rodar análises em paralelo
        with ThreadPoolExecutor() as executor:
            futures = {
                'conditions': executor.submit(self.conditions, content),
                'vulnerabilities': executor.submit(self.vulnerabilities, content),
                'workflow_dispatch': executor.submit(self.workflow_dispatch, content),
                'global_variables': executor.submit(self.global_variables, content)
            }

            for key, future in futures.items():
                analyses[key] = future.result()

        return analyses
