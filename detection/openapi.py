OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Object Detection API",
        "description": "This API performs object detection on the provided image using an ONNX model.",
        "version": "0.1.0",
    },
    "paths": {
        "/": {
            "get": {
                "summary": "Get OpenAPI Specification",
                "description": "Returns the OpenAPI specification for this API.",
                "responses": {
                    "200": {
                        "description": "OpenAPI specification returned successfully",
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    }
                },
            },
            "post": {
                "summary": "Detect Objects",
                "description": "Performs object detection on a provided base64 encoded image.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "image": {
                                        "type": "string",
                                        "description": "Base64 encoded image string. Must not include the data URI scheme prefix (e.g., 'data:image/jpeg;base64,').",
                                    },
                                    "conf_thres": {
                                        "type": "number",
                                        "format": "float",
                                        "default": 0.7,
                                        "minimum": 0.0,
                                        "maximum": 1.0,
                                        "description": "Confidence threshold for detections.",
                                    },
                                    "iou_thres": {
                                        "type": "number",
                                        "format": "float",
                                        "default": 0.5,
                                        "minimum": 0.0,
                                        "maximum": 1.0,
                                        "description": "Intersection over Union (IoU) threshold for Non-Maximum Suppression (NMS).",
                                    },
                                    "save_image": {
                                        "type": "boolean",
                                        "default": False,
                                        "description": "Whether to save the uploaded image and its detections to S3.",
                                    },
                                },
                                "required": ["image"],
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful detection response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "detections": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "bbox": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "description": "Bounding box coordinates [x_min, y_min, x_max, y_max]",
                                                    },
                                                    "score": {
                                                        "type": "number",
                                                        "format": "float",
                                                        "description": "Confidence score of the detection",
                                                    },
                                                    "class_id": {
                                                        "type": "integer",
                                                        "description": "ID of the detected class",
                                                    },
                                                    "class_name": {
                                                        "type": "string",
                                                        "description": "Name of the detected class",
                                                    },
                                                },
                                            },
                                        },
                                        "version": {
                                            "type": "string",
                                            "description": "API Version",
                                        },
                                        "image_url": {
                                            "type": "string",
                                            "description": "S3 URL of the saved image (provided only if save_image was true)",
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "400": {
                        "description": "Bad Request - Invalid input parameters or missing fields",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {
                                            "type": "string",
                                            "description": "Error message describing the invalid input",
                                        }
                                    },
                                }
                            }
                        },
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "description": "Error message describing the server issue",
                                        }
                                    },
                                }
                            }
                        },
                    },
                },
            },
            "options": {
                "summary": "CORS Preflight",
                "description": "Handles CORS preflight requests.",
                "responses": {
                    "200": {
                        "description": "CORS preflight successful",
                        "headers": {
                            "Access-Control-Allow-Origin": {
                                "schema": {"type": "string"}
                            },
                            "Access-Control-Allow-Methods": {
                                "schema": {"type": "string"}
                            },
                            "Access-Control-Allow-Headers": {
                                "schema": {"type": "string"}
                            },
                        },
                    }
                },
            },
        }
    },
}
