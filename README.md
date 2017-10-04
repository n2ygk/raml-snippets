# RAML snippets

Some useful RAML 1.0 snippets.

- [Introduction](#introduction)
- [JSON API 1.0](#json-api-10-libraries)
- [OAuth 2.0 types library](oauth-20-types-library)
- [Example](#example)
- [Issues](#issues)
- [TO DO](#to-do)
- [Author](#author)
- [LICENSE](#license)

## Introduction

Find here some useful RAML 1.0 snippets (mostly as RAML 1.0 Libraries) that can be
included in your root RAML API document.

## JSON API 1.0 Libraries

### jsonApiLibrary.raml: request/reply type definitions library

This [library](libraries/jsonApiLibrary.raml) defines RAML types for [{json:api} 1.0](http://jsonapi.org/format) RESTful API
requests and responses.

This library of RAML types is derived directly from the json-api 1.0 [specification](https://github.com/json-api/json-api/blob/gh-pages/schema)
which is coded using the [json-schema.org](http://json-schema.org/documentation.html) specification. 

See the related jsonApiCollections.raml Library for useful resourceTypes and traits that use these types.

Jsonapi uses [mediatype](https://www.iana.org/assignments/media-types/application/vnd.api+json)
`application/vnd.api+json` in requests and responses. 

Example usage:
```
uses:
  api: jsonApiLibrary.raml
...
/widgets:
  get:
    responses: 
      200:
        body: 
          application/vnd.api+json:
            type: api.success
            properties: 
              data: widget[]
```
  
Make your API-specific `data` types subclasses of api.resource and your methods should use type api.success
for successful responses, api.failure for failure responses and api.info for where only the `meta` attribute
is required in a response (e.g. 200 response to a DELETE).
  
### jsonApiCollections.raml: collection-item resourceTypes and traits library

This is a companion to the jsonApiLibrary.raml Library. Types definined in
that library are used here to define collections and items and their associated
methods and body mediatypes (application/vnd.api+json).

Collection: GET, POST

Item: GET, PATCH, DELETE

Jsonapi does not define a PUT method, preferring PATCH.

Example usage:
```
uses:
  col: libraries/jsonApiCollections.raml

...
/widgets:
  displayName: widgets
  description: stuff we have in inventory
  type: 
    col.collection: 
      dataType: wid.Widget
      exampleCollection: !include examples/WidgetCollectionExample.raml
      exampleItem: !include examples/WidgetItemExample.raml
```

## OAuth 2.0 types library

The [OAuth 2.0 types library](libraries/oAuth2Types.raml) currently only defines the
`success` and `error` types for the token request endpoint.

## Example

An example of using the JSON API libraries consists of the following RAML files:

- [Root API](api.raml) -- top-level RAML 1.0 API definition.
- [Columbia securitySchemes and traits Library](libraries/columbiaLibrary.raml) -- locally-defined standards.
- [example Widget type definition](libraries/WidgetType.raml) -- subclasses JSON API `resource` and `attributes` types.
- [exampl Location type definition](libraries/LocationType.raml) -- another user API type.

Using the above-defined types, resourceTypes, and traits, we are able stay DRY and have
a pretty concise root API document that focuses on what's unique about this API, 
reusing standard patterns for OAuth 2.0-protected resources that follow the JSON API 1.0 spec.

```
#%RAML 1.0
title: demo-jsonapi
description: a sample RESTful API that conforms to jsonapi.org 1.0
version: v1
#...
uses: 
  api: libraries/jsonApiLibrary.raml
  loc: libraries/LocationType.raml
  wid: libraries/WidgetType.raml
  col: libraries/jsonApiCollections.raml
  cu: libraries/columbiaLibrary.raml

# the API's resources:
/widgets:
  displayName: widgets
  description: stuff we have in inventory
  type: 
    col.collection: 
      dataType: wid.Widget
      exampleCollection: !include examples/WidgetCollectionExample.raml
      exampleItem: !include examples/WidgetItemExample.raml
  get:
    is: 
      - cu.oauth_read_any
  post:
    is: 
      - cu.oauth_create_any
```

## Issues

### RAML 1.0 types instead of JSON Schemas

While we would have liked to use [json-schema.org](http://json-schema.org/documentation.html)
representations for types, RAML 1.0
[does not support type inheritance for JSON schemas](https://github.com/raml-org/raml-spec/blob/master/versions/raml-10/raml-10.md#using-xml-and-json-schema):

_A RAML processor MUST NOT allow types that define an XML or JSON
schema to participate in type inheritance or specialization, or
effectively in any type expression. Therefore, you cannot define
sub-types of these types to declare new properties, add
restrictions, set facets, or declare facets. You can, however,
create simple type wrappers that add annotations, examples, display
name, or a description._

Luckily the RAML 1.0 type system is based on json-schema.org so it is easy to generate
json-schema.org from the RAML type definitions.

### Only way to get the metadata is via parsing RAML

There appears to be no standard way to identify the metadata for a RAML 1.0 API as part of the API
definition (e.g. as a well-known resource; Mulesoft's APIkit uses `/console/api/?raml` but this is
not even documented anywhere and is not in the API's resource namespace). There is a dearth of client
libraries that can parse compound RAML 1.0 documents (e.g. using libraries and other RAML fragments)
into a compiled JSON representation. One that works well for javascript is
[raml-json-enhance-node](https://github.com/mulesoft-labs/raml-json-enhance-node). It compiles
the RAML 1.0 to [this JSON schema](https://github.com/raml-org/raml-js-parser-2/tree/master/tckJSONSchema-newFormat/spec-1.0).

Perhaps this will be made moot by adoption of Open API 3.0.

### RAML 1.0 types are not resolvable into schemas

Even though jsonapi requires a `type` attribute (as does RAML 1.0), there is no standard place
to find type definitions. Json-schema.org uses `"{$ref": "#/definitions/<type>"}`
-- a [JSON pointer](https://tools.ietf.org/html/rfc6901) -- for this.

## TO DO

Still to do:
- Define a local standard for finding API metadata if a global standard isn't available.
- Refactor for [OAS 3.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md)

## Author
Alan Crosswell

Copyright (c) 2017 The Trustees of Columbia University in the City of New York

## LICENSE

Licensed under the [Apache License, Version 2.0](LICENSE) (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.


