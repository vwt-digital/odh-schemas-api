import json

from google.cloud import storage


class GCSProcessor:
    def __init__(self, catalog_bucket_name):
        self.stg_client = storage.Client()
        self.topic_schemas = self.retrieve_topic_schemas(catalog_bucket_name)

    def retrieve_topic_schemas(self, bucket_name):
        """
        Retrieve a list of Topics with schemas from the Data Catalogs

        :param bucket_name: Bucket name
        :type bucket_name: str

        :return: List of topics with schemas
        :rtype: dict
        """

        bucket = self.stg_client.get_bucket(bucket_name)
        blobs = self.stg_client.list_blobs(bucket)

        topics_with_schema = {}

        for blob in blobs:
            try:
                blob_json = json.loads(blob.download_as_string())
            except ConnectionError:
                continue
            else:
                for dataset in blob_json.get("dataset", []):
                    for distribution in dataset.get("distribution", []):
                        if (
                            distribution["format"] == "topic"
                            and "describedBy" in distribution
                            and "describedByType" in distribution
                        ):
                            topics_with_schema[distribution["title"]] = {
                                "describedBy": distribution["describedBy"],
                                "describedByType": distribution["describedByType"],
                            }

        return topics_with_schema

    def retrieve_schema(self, bucket_name, schema_name):
        """
        Retrieve the schema

        :param bucket_name: Bucket name
        :type bucket_name: str
        :param schema_name: Schema name
        :type schema_name: str

        :return: Schema
        """

        schema_file_name = schema_name.replace("/", "_")
        bucket = self.stg_client.get_bucket(bucket_name)

        if storage.Blob(bucket=bucket, name=schema_file_name).exists(self.stg_client):
            try:
                blob = bucket.blob(schema_file_name)
                return blob.download_as_string()
            except ConnectionError:
                return None

        return None
