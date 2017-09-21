#!/usr/bin/env python3
"""
Convert JSON Schema to YAML. Useful for converting json:api 1.0 schema, for example.
Example: json2api jsonapi.json >jsonapi.yaml
"""
import sys, json, yaml

with open(sys.argv[1]) as f:
    print(yaml.safe_dump(json.load(f), default_flow_style=False))

