import logging
import re

import config
from storage_processor import GCSProcessor

logging.getLogger().setLevel(logging.INFO)

# Retrieve list of topic schemas on init
gcs_processor = GCSProcessor(config.BUCKET_DATA_CATALOGS)
logging.info(f"Pre-loaded {len(gcs_processor.topic_schemas)} topics")


def schemas_api(request):
    """
    Retrieve the schema based on the request

    :param request: Request object

    :return: Schema
    """

    if not re.match(r"/schemas/([a-zA-Z-]*)", request.path):
        return "Bad Request", 400

    key = request.path[9:]  # remove the /schemas/

    if key in gcs_processor.topic_schemas:
        schema = gcs_processor.retrieve_schema(
            config.BUCKET_SCHEMAS, gcs_processor.topic_schemas[key]["describedBy"]
        )

        if schema:
            return schema, 200, {"Content-Type": "application/json"}

    return "Not Found", 404, {"Content-Type": "application/json"}
