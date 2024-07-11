import csv
import re
import platform


class Config:
    """
    A class that contains utility methods.

    Attributes:
        csv_path (str): The path to the CSV file containing repository URLs.
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path

    @classmethod
    def handle_none(cls, value):
        return "None" if value is None else value

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

    def reading_repos(self, url_column):
        """
        Reads the CSV file containing repository URLs.

        Yields:
            str: The URL of each repository read from the CSV file.
        """
        with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)
            for row in reader:
                repo_url = row[url_column]
                yield repo_url

    @staticmethod
    def get_base_directory():
        system = platform.system()
        if system == 'Windows':
            return "C:\\Generated"
        elif system == 'Linux' or system == 'Darwin':
            return "/root/Generated"
        else:
            raise Exception("Unsupported operating system")


class Lists:
    """
    A class that contains dictionaries for the smells and the smells' abbreviations.
    """

    keywords = [
        "API_KEY", "ACCESS_KEY", "SECRET_KEY", "PASSWORD", "TOKEN", "PRIVATE_KEY", "PUBLIC_KEY", "CLIENT_ID",
        "CLIENT_SECRET", "SSH_KEY", "SSH_PRIVATE_KEY", "SSH_PUBLIC_KEY", "DB_PASSWORD", "DB_USER", "DB_USERNAME",
        "DB_SECRET", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET",
        "AZURE_SUBSCRIPTION_ID", "AZURE_TENANT_ID", "GOOGLE_APPLICATION_CREDENTIALS", "GCP_PROJECT_ID",
        "GCP_PRIVATE_KEY", "GCP_CLIENT_EMAIL", "GCP_CLIENT_ID", "DO_ACCESS_TOKEN", "DIGITALOCEAN_ACCESS_TOKEN",
        "GITHUB_TOKEN", "GITLAB_TOKEN", "DOCKER_PASSWORD", "DOCKER_USERNAME", "KUBE_CONFIG", "KUBECONFIG",
        "SMTP_PASSWORD", "SMTP_USER", "SMTP_USERNAME", "SMTP_SECRET", "SLACK_TOKEN", "SLACK_WEBHOOK_URL",
        "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "PAYPAL_CLIENT_ID", "PAYPAL_CLIENT_SECRET", "STRIPE_SECRET_KEY",
        "STRIPE_PUBLISHABLE_KEY", "SENTRY_DSN", "SENTRY_AUTH_TOKEN", "MONGODB_URI", "MONGODB_PASSWORD",
        "MONGODB_USER", "MONGODB_USERNAME", "REDIS_PASSWORD", "REDIS_USER", "REDIS_USERNAME", "POSTGRES_PASSWORD",
        "POSTGRES_USER", "POSTGRES_USERNAME", "MYSQL_PASSWORD", "MYSQL_USER", "MYSQL_USERNAME", "INFLUXDB_TOKEN",
        "INFLUXDB_USER", "INFLUXDB_USERNAME", "INFLUXDB_PASSWORD", "RABBITMQ_USER", "RABBITMQ_USERNAME",
        "RABBITMQ_PASSWORD", "NPM_TOKEN", "NPM_AUTH_TOKEN", "GITLAB_RUNNER_TOKEN", "HEROKU_API_KEY", "HEROKU_APP_NAME",
        "FIREBASE_API_KEY", "FIREBASE_AUTH_DOMAIN", "FIREBASE_PROJECT_ID", "FIREBASE_STORAGE_BUCKET",
        "FIREBASE_MESSAGING_SENDER_ID", "FIREBASE_APP_ID", "FIREBASE_MEASUREMENT_ID", "MAPBOX_ACCESS_TOKEN",
        "ALGOLIA_API_KEY", "ALGOLIA_APP_ID", "SEGMENT_WRITE_KEY", "NETLIFY_AUTH_TOKEN", "NETLIFY_SITE_ID",
        "SENDGRID_API_KEY", "MAILGUN_API_KEY", "MAILGUN_DOMAIN", "MAILGUN_SECRET", "MAILCHIMP_API_KEY",
        "MAILCHIMP_SERVER_PREFIX", "GIT_TOKEN", "CIRCLECI_API_TOKEN", "BITBUCKET_CLIENT_ID", "BITBUCKET_CLIENT_SECRET",
        "DISCORD_TOKEN", "TELEGRAM_BOT_TOKEN", "TRELLO_KEY", "TRELLO_TOKEN", "SPOTIFY_CLIENT_ID",
        "SPOTIFY_CLIENT_SECRET", "YOUTUBE_API_KEY", "GOOGLE_MAPS_API_KEY", "PAGERDUTY_API_TOKEN", "NEWRELIC_API_KEY",
        "NEWRELIC_INSERT_KEY", "AIRTABLE_API_KEY", "NOTION_API_KEY", "ASANA_ACCESS_TOKEN", "LINE_CHANNEL_SECRET",
        "LINE_CHANNEL_ACCESS_TOKEN", "SALESFORCE_CLIENT_ID", "SALESFORCE_CLIENT_SECRET", "SALESFORCE_USERNAME",
        "SALESFORCE_PASSWORD", "SALESFORCE_TOKEN", "SAP_PASSWORD", "SAP_USER", "SAP_USERNAME", "JIRA_API_TOKEN",
        "JIRA_USERNAME", "JIRA_PASSWORD", "CONFLUENCE_API_TOKEN", "CONFLUENCE_USERNAME", "CONFLUENCE_PASSWORD",
        "HUBSPOT_API_KEY", "ZAPIER_API_KEY", "ZENDESK_API_KEY", "ZENDESK_USERNAME", "ZENDESK_PASSWORD",
        "SERVICENOW_API_KEY", "SERVICENOW_USERNAME", "SERVICENOW_PASSWORD", "OKTA_CLIENT_ID", "OKTA_CLIENT_SECRET",
        "OKTA_API_TOKEN", "PIVOTAL_TRACKER_API_TOKEN", "TOTP_SECRET", "OTP_SECRET", "LAMBDA_API_KEY",
        "CLOUDFLARE_API_KEY", "CLOUDFLARE_API_TOKEN", "CLOUDFLARE_EMAIL", "CLOUDFLARE_ACCOUNT_ID",
        "CLOUDFRONT_KEY_PAIR_ID", "CLOUDFRONT_PRIVATE_KEY", "CLOUDBEES_API_KEY", "CLOUDBEES_SECRET", "CLOUDBEES_USER",
        "CLOUDBEES_USERNAME", "BITRISE_API_TOKEN", "SENTRY_API_KEY", "CODECOV_TOKEN", "SEMAPHORE_API_TOKEN",
        "WERCKER_API_TOKEN", "APPCENTER_TOKEN", "TESTFAIRY_API_KEY", "FASTLANE_PASSWORD", "FASTLANE_USERNAME",
        "APPVEYOR_API_TOKEN", "TRAVIS_API_TOKEN", "COVERALLS_REPO_TOKEN", "NEWRELIC_ACCOUNT_ID", "NEWRELIC_API_KEY"
    ]
    regex_patterns = [
        r'\bsecret\b', r'\bkey\b', r'\btoken\b', r'\bpassword\b', r'\bpwd\b', r'\baccess\b', r'\bprivate\b', r'\bssh\b',
        r'\bpassphrase\b', r'\bcredential\b', r'\bapi\b', r'\bauth\b', r'\bsalt\b', r'\bencryption\b', r'\bmaster\b',
        r'\bclient_id\b', r'\bclient_secret\b', r'\bdb_user\b', r'\bdb_password\b', r'\bdatabase_url\b',
        r'\bprivate_key\b',
        r'\bpublic_key\b', r'\baws_access_key\b', r'\baws_secret_key\b', r'\bgcp_keyfile\b', r'\bazure_client_id\b',
        r'\bazure_secret\b', r'\bdo_token\b', r'\bgithub_token\b', r'\bslack_token\b', r'\btwilio_auth_token\b',
        r'\bsendgrid_api_key\b', r'\bmailgun_api_key\b', r'\bjwt_secret\b', r'\bjwt_key\b', r'\boauth_token\b',
        r'\bdropbox_secret\b', r'\bheroku_api_key\b', r'\bsparkpost_api_key\b', r'\bftp_password\b', r'\bftp_user\b',
        r'\bpaypal_secret\b', r'\bstripe_secret_key\b', r'\bstripe_publishable_key\b', r'\balgolia_api_key\b',
        r'\bamplitude_api_key\b', r'\bfacebook_app_id\b', r'\bfacebook_app_secret\b', r'\bgoogle_client_id\b',
        r'\bgoogle_client_secret\b', r'\binstagram_client_id\b', r'\binstagram_client_secret\b',
        r'\blinkedin_client_id\b',
        r'\blinkedin_client_secret\b', r'\btwitter_api_key\b', r'\btwitter_api_secret\b', r'\bgithub_client_id\b',
        r'\bgithub_client_secret\b', r'\breddit_client_id\b', r'\breddit_client_secret\b', r'\bspotify_client_id\b',
        r'\bspotify_client_secret\b', r'\btumblr_consumer_key\b', r'\btumblr_consumer_secret\b',
        r'\bdiscord_client_id\b',
        r'\bdiscord_client_secret\b', r'\bgitlab_private_token\b', r'\bbitbucket_client_id\b',
        r'\bbitbucket_client_secret\b',
        r'\bcoinbase_api_key\b', r'\bcoinbase_api_secret\b', r'\bshopify_api_key\b', r'\bshopify_api_secret\b',
        r'\btrello_api_key\b', r'\btrello_token\b', r'\bwordpress_client_id\b', r'\bwordpress_client_secret\b',
        r'\byoutube_api_key\b', r'\byoutube_api_secret\b', r'\bsendinblue_api_key\b', r'\bmailchimp_api_key\b',
        r'\belasticsearch_password\b', r'\belasticsearch_user\b', r'\bsmtp_password\b', r'\bsmtp_user\b',
        r'\bjenkins_password\b', r'\bjenkins_user\b', r'\bredis_password\b', r'\bredis_user\b',
        r'\bmysql_root_password\b',
        r'\bmysql_user\b', r'\bmysql_password\b', r'\bpostgres_user\b', r'\bpostgres_password\b', r'\bmongodb_uri\b',
        r'\bcloudinary_api_key\b', r'\bcloudinary_api_secret\b', r'\bmapbox_access_token\b',
        r'\bcontentful_access_token\b',
        r'\btotp_secret\b', r'\bapi_secret\b', r'\bconsumer_secret\b', r'\bvault_password\b', r'\bvault_token\b',
        r'\bb2_app_key\b', r'\bb2_app_key_id\b', r'\bb2_bucket_name\b', r'\bb2_bucket_id\b', r'\bb2_account_id\b',
        r'\bb2_account_key\b', r'\bnetlify_access_token\b', r'\bvultr_api_key\b', r'\blinode_api_key\b',
        r'\bheroku_api_token\b',
        r'\bfastly_api_key\b', r'\bneo4j_password\b', r'\bneo4j_user\b', r'\bcouchdb_user\b', r'\bcouchdb_password\b',
        r'\binfluxdb_user\b', r'\binfluxdb_password\b', r'\bmemcached_user\b', r'\bmemcached_password\b',
        r'\brabbitmq_user\b',
        r'\brabbitmq_password\b', r'\bsonarqube_token\b', r'\btravis_token\b', r'\bdrone_token\b',
        r'\bsemaphore_token\b',
        r'\bcircleci_token\b', r'\bcodeship_token\b', r'\bgitlab_token\b'
    ]
    permissions = ["write", "write-all"]
