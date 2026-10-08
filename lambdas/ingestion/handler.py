from __future__ import annotations

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    processed = 0
    for record in event.get("Records", []):
        body = json.loads(record.get("body", "{}"))
        logger.info("document_event=%s", body)
        processed += 1
    return {"statusCode": 200, "processed": processed}
