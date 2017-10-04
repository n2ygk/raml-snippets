# RAML snippets

Some useful RAML 1.0 snippets.

- [Introduction](#introduction)
- [JSON API 1.0](#json-api-10-libraries)
- [OAuth 2.0 types library](oauth-20-types-library)
- [Example](#example)
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

See the related jsonApiCollections.raml Library for useful resourceTypes and traits that uses these types.

Jsonapi uses mediatype `application/vnd.api+json` in requests and responses. 

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
for successful responses and api.failure for failure responses.
  
### jsonApiCollections.raml: collection-item resourceTypes and traits library

This is a companion to the jsonApiLibrary.raml Library. Types definined in
that library are used here to define collections and items and their associated
methods and body mediatypes (application/vnd.api+json).

Collection: get, post

Item: get, patch, delete

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

The [OAuth 2.0 types library](libraries/oAuth2Types.raml) defines the
`success` and `error` types.

## Example

An example of using the JSON API libraries consists of the following RAML files:

- [Root API](api.raml)
- [Columbia securitySchemes and traits Library](libraries/columbiaLibrary.raml)
- [Widget type definition](libraries/WidgetType.raml) -- subclasses JSON API `resource` and `attributes` types.
- [Location type definition](libraries/LocationType.raml) -- another user API type.

Using the above-defined types, resourceTypes, and traits, we are able to DRY and have
a pretty concise root API document that focuses on what's unique about this API and
reuses are standard patterns for OAuth 2.0-protected resources that follow the JSON API 1.0 spec.

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

## TO DO

Still to do:
- Add JSON API traits for filtering, sorting, paging.
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


