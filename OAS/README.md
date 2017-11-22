# RAML to OAS and vice-versa
## OAS 3.0 spec

https://swagger.io/docs/specification/basic-structure/

https://swagger.io/specification/

## RAML 1.0 to OAS 3.0 conversion

See https://github.com/mulesoft/oas-raml-converter

```sh
cd ..
git clone git@github.com:mulesoft/oas-raml-converter.git
cd oas-raml-converter
npm run build
npm install -g
cd ../raml-snippets/OAS
oas-raml-converter --from RAML --to OAS30 ../api.raml >openapi.json
```

## Swagger Editor only supports Swagger 2.0

See https://github.com/swagger-api/swagger-editor/releases

```sh
npm install -g http-server
wget https://github.com/swagger-api/swagger-editor/archive/v3.1.16.zip
unzip swagger-editor.zip
http-server swagger-editor
```

## Code Generator

Nothing yet in swagger-codegen. See this: https://github.com/mermade/openapi-codegen
