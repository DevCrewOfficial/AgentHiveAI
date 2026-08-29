import mock_sys


def get_shipment_status(shipment_id: str):
    return mock_sys.get_shipment_status(shipment_id)


def reschedule_delivery(shipment_id: str, new_date: str):
    return mock_sys.reschedule_delivery(shipment_id, new_date)


def redirect_shipment(shipment_id: str, new_address: str):
    return mock_sys.redirect_shipment(shipment_id, new_address)


def initiate_replacement(shipment_id: str):
    return mock_sys.initiate_replacement(shipment_id)


def request_missing_document(shipment_id: str, doc_type: str):
    return mock_sys.request_missing_document(shipment_id, doc_type)


def notify_customer(shipment_id: str, message: str):
    return mock_sys.notify_customer(shipment_id, message)


def create_ops_ticket(shipment_id: str, reason: str):
    return mock_sys.create_ops_ticket(shipment_id, reason)


def escalate_to_human(shipment_id: str, reason: str):
    return mock_sys.escalate_to_human(shipment_id, reason)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_shipment_status",
            "description": "Check the current status, address, ETA, value, and damage status of a shipment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {
                        "type": "string",
                        "description": "Shipment ID such as SHIP001"
                    }
                },
                "required": ["shipment_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reschedule_delivery",
            "description": "Reschedule a shipment delivery to a new date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string"},
                    "new_date": {"type": "string"}
                },
                "required": ["shipment_id", "new_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "redirect_shipment",
            "description": "Change the delivery address of a shipment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string"},
                    "new_address": {"type": "string"}
                },
                "required": ["shipment_id", "new_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "initiate_replacement",
            "description": "Initiate a replacement for a shipment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string"}
                },
                "required": ["shipment_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "request_missing_document",
            "description": "Request a missing document from the customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string"},
                    "doc_type": {"type": "string"}
                },
                "required": ["shipment_id", "doc_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notify_customer",
            "description": "Send a notification to the customer about a shipment action.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["shipment_id", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_ops_ticket",
            "description": "Create an operations ticket for a shipment issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["shipment_id", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Escalate a shipment issue to a human operations agent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["shipment_id", "reason"]
            }
        }
    }
]


FUNCTIONS = {
    "get_shipment_status": get_shipment_status,
    "reschedule_delivery": reschedule_delivery,
    "redirect_shipment": redirect_shipment,
    "initiate_replacement": initiate_replacement,
    "request_missing_document": request_missing_document,
    "notify_customer": notify_customer,
    "create_ops_ticket": create_ops_ticket,
    "escalate_to_human": escalate_to_human,
}