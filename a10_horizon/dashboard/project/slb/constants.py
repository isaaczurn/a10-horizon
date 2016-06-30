# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.

OP_DICT = {
    ">": "greater than",
    "<": "less than",
    ">=": "greater than or equal to",
    "<=": "less than or equal to",
}

AGG_DICT = {
    "avg": "average",
    "sum": "sum",
    "min": "minimum",
    "max": "maximum"
}

UNIT_DICT = {
    "count": "",
    "percentage": "%",
    "bytes": "bytes",
}

MEASUREMENTS = [
    "connections",
    "cpu",
    "interface",
    "memory"
]

VALID_MEASUREMENT_UNITS = {
    "connections": ["count"],
    "cpu": ["percentage"],
    "interface": ["percentage", "count"],
    "memory": ["bytes", "percentage"],
}
