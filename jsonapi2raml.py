#!/usr/bin/env python3
"""
Convert {json:api} 1.0 schema (represented in json-schema) to RAML 1.0 types.
Example: jsonapi2ramli jsonapi.json >jsonapi.raml

"definitions" are turned into types.
$ref are dereferenced to the types they reference.
Since RAML accepts json-schema as input, the key names are basically the same
"""
import sys, json, yaml
from pprint import pprint, pformat

with open('jsonapi.json','r') as f:
    schema=json.load(f)

if '$schema' in schema and schema['$schema'] != 'http://json-schema.org/draft-04/schema#':
    print('Unexpected json-schema.org schema: %s'%schema['$schema'])
    exit(1)

definitions = schema['definitions']

# starting dumping out the types
if 'title' in schema:
    print('# %s'%schema['title'])
if 'description' in schema:
    print('# %s'%schema['description'])
# ironically, there is no version for JSON API in it's own schema.

print('types:')
for typename,v in definitions.items():
    print('  %s:'%typename)
    required = v['required'] if 'required' in v else {}
    if 'type' in v:
        print('    type: %s'%v['type'])
    if 'additionalProperties' in v:
        print('    additionalProperties: %s'%("true" if v['additionalProperties'] else "false"))
    properties = v['properties'] if 'properties' in v else {}
    if properties:
        print('    properties:')
    for propname,propval in properties.items():
        print('      %s:'%propname)
        print('        required: %s'%('true' if propname in required else 'false'))
        if isinstance(propval,str):
            print('        %s'%propval)
        elif isinstance(propval,dict):
            for key,val in propval.items():
                if isinstance(val,dict): # here we go again. I should recurse.
                    #print('## dict: %s %s len %d'%(val,type(val),len(val)))
                    if key == 'items' and '$ref' in val:
                        print('        items: %s'%val['$ref'].replace('#/definitions/',''))
                    else:
                        print('        %s:'%key)
                        # it's probably an object definition
                        for key2,val2 in val.items():
                            print('          %s:'%key2)
                            if isinstance(val2,dict):
                                for key3,val3 in val2.items():
                                    print('            %s: %s'%(key3,val3))
                            else:
                                print('          %s: %s'%(key2,val2))
                else:
                    if key == '$ref': # reference to another type
                        val = val.replace('#/definitions/','')
                        key = 'type'
                    elif key == 'allOf': # all these types
                        print('## allOf')
                    elif key == 'oneOf': # any of these types
                        print('## oneOf')
                    elif key == 'anyOf': # any of these types
                        print('## anyOf')
                    print('        %s: %s'%(key,val))
