import logging
import re

import config
from storage_processor import GCSProcessor

logging.getLogger().setLevel(logging.INFO)

# Retrieve list of topic schemas on init
gcs_processor = GCSProcessor(config.BUCKET_DATA_CATALOGS)
logging.info(f"Pre-loaded {len(gcs_processor.topic_schemas)} topics with schemas")


def schemas_api(request):
    """
    Retrieve the schema based on the request

    :param request: Request object

    :return: Schema
    """

    if not re.match(r"/schemas/([a-zA-Z-]*)", request.path):
        return "Bad Request", 400, {"Content-Type": "application/json"}

    key = request.path[9:]  # remove the /schemas/
    content_type = request.headers.get("accept", "application/json")

    if content_type not in ["application/json", "application/xml"]:
        logging.info(
            f"Requesting 'schemas/{key}' in unsupported format '{content_type}', returning"
        )
        return "Unsupported Accept-Type", 415, {"Content-Type": "application/json"}

    logging.info(f"Requesting 'schemas/{key}' in format '{content_type}'")
    if key in gcs_processor.topic_schemas:
        try:
            schema = gcs_processor.retrieve_schema(
                config.BUCKET_SCHEMAS,
                gcs_processor.topic_schemas[key]["describedBy"],
                content_type,
            )
        except (ConnectionError, TypeError) as e:
            logging.error(
                f"Error when retrieving 'schemas/{key}' in format '{content_type}': {str(e)}"
            )
            return "Bad Request", 400, {"Content-Type": "application/json"}
        else:
            if schema:
                logging.info(f"Returning 'schemas/{key}' in format '{content_type}'")
                return schema, content_type

    logging.info(f"Could not find 'schemas/{key}'")
    return "Not Found", 404, {"Content-Type": "application/json"}
