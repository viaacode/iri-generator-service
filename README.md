# IRI generator service

This application runs a Web service that dispenses NOIDs or IRIs to applications.
It can create multiple independent minters that are capable to mint and persist NOIDs. Minters can also bind minted NOIDs to a string for later retrieval. 
The NOID generator uses [noid](https://pypi.org/project/noid/) for minting NOIDs, and PostgreSQL for persisting all minter configurations and the minted NOIDs with minimal metadata, such as their bindings.

## Testing and development

This repo uses Docker (Compose) to run the test and development environment. 

### Run the tests

```
bash scripts/run-tests.sh
```

### Run the development setup

```
bash scripts/run-dev.sh
```

## Configuration

| Variable | Description | Default |
| ----- | ----- | --- |
| POSTGRES_HOST | The host URL of the postgres database. | `"0.0.0.0"` |
| POSTGRES_USER | The user of the postgres database. | `"postgres"` |
| POSTGRES_PASSWORD | The password of the postgres database. | `"postgres"` |
| POSTGRES_DB | The name of the postgres scheme. | `"postgres"` |
| POSTGRES_PORT | The port the postgres instance is running on. |`5432` |
| POSTGRES_ECHO | | `false` |
| POSTGRES_POOL_SIZE | The size of the postgres connection pool. | `5` |
| NOID_SCHEME | The default NOID scheme. | `""` |
| NOID_TEMPLATE | The default template by which to generate NOIDs. See [](https://metacpan.org/dist/Noid/view/noid#TEMPLATES) for more information on how to construct templates. | `"zedededek"` |
| NOID_NAA | The default name assigning authority (NAA) number. | `""` |

## API

The API is documented using openapi located at `/docs`.

### Creating a new minter

You can create a new minter by executing `POST` to `/api/v1/minters/`. 
The configuration for the minter can be supplied with a JSON payload, containing the noid scheme [default: `NOID_SCHEME`], the name assigning authority (NAA) number [default: `NOID_NAA`], and the template by which to generate NOIDs [default: `NOID_TEMPLATE`]. Note that the combination of scheme, naa and template must be unique to prevent different minters minting clashing NOIDs.
An example payload is given below:

```json
{
    "scheme": "", 
    "naa": "",
    "template": "zedededek",
}
```
This will return the configuration of the created minter identified by an UUID. 
For example, the request above could result into something like 

```json
{
    "scheme": "",
    "naa": "",
    "template": "zedededek",
    "last_n": 0,
    "created_at": "2023-09-28T14:26:13.537514",
    "updated_at": "2023-09-28T14:26:13.537525",
    "id": "065158d0-5899-7d79-8000-eac0bd0a47c1"
}
```

The minter is now available at `/api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/`. 

### Creating a URI minter

You can create a minter that generates URIs by setting the scheme of the minter to any URI base. 
For instance, the following configuration will create a minter that mints NOIDs that look like `https://example.org/0000004t`.

```json
{
    "scheme": "https://example.org/", 
    "template": "zedededek"
}
```


### Creating one or more NOIDs

Once you have created a minter, you can use it to mint new noids. 
To create one or more new NOIDs, run a `POST` to `/api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/` and it will mint a new NOID every time.
For example:

```json
[
  {
    "binding": null,
    "created_at": "2023-09-29T09:35:44.897002",
    "updated_at": "2023-09-29T09:35:44.897011",
    "id": "065169a7-0e5a-72e5-8000-9187bb9dbe19",
    "noid": "00000000",
    "n": 0,
    "minter_id": "065169a6-4f2e-79b2-8000-75d456308644"
  }
]
```

In case you need multiple noids, add the `count` query parameter like:

```
POST /api/v1/minters/065169a6-4f2e-79b2-8000-75d456308644/noids/?count=3
```

Which will yield

```json
[
  {
    "binding": null,
    "created_at": "2023-09-29T09:36:13.908365",
    "updated_at": "2023-09-29T09:36:13.908370",
    "id": "065169a8-de88-7b34-8000-dd6c6d43c559",
    "noid": "00000017",
    "n": 1,
    "minter_id": "065169a6-4f2e-79b2-8000-75d456308644"
  },
  {
    "binding": null,
    "created_at": "2023-09-29T09:36:13.908621",
    "updated_at": "2023-09-29T09:36:13.908623",
    "id": "065169a8-de89-7ba6-8000-0b00eca1a290",
    "noid": "0000002e",
    "n": 2,
    "minter_id": "065169a6-4f2e-79b2-8000-75d456308644"
  },
  {
    "binding": null,
    "created_at": "2023-09-29T09:36:13.908780",
    "updated_at": "2023-09-29T09:36:13.908782",
    "id": "065169a8-de8a-760b-8000-9b07c733c81b",
    "noid": "0000003m",
    "n": 3,
    "minter_id": "065169a6-4f2e-79b2-8000-75d456308644"
  }
]
```

You can retrieve the metadata of a NOID by doing a `GET`:

```http
GET /api/v1/minters/065169a6-4f2e-79b2-8000-75d456308644/noids/0000003m
```

To retrieve the NOIDs that match a particular binding:

```
GET /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids?binding=key
```

### Binding a key to a pre-existing NOID

You can also bind any string to a NOID in case you need to reproduce it.
For example, binding the NOID `00` to `key`
```
PUT /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/00?binding=key
```

Note that the noid, in this case `00`, should be created first by using, for example, `POST` on `/api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/`.

<!-- You can retrieve the binding by doing

```
GET /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/00/binding/
``` -->

To retrieve the same NOID, do

```
GET /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids?binding=key
```

Or

```
GET /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/bind/key
```

You can also unset a binding by doing

```
DELETE /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/00?binding
```

Note that the API does not allow you to delete or alter NOIDs expect for the binding. 
PUT or DELETE requests on a `/noids/{noid}` on a will return a `405` if the binding parameter is not supplied.

### Binding a key to a new NOID

It is also possible to create and bind nodes at the same time. 
For example:

```
POST /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/bind/
```

with payload:

```json
{ "bindings": "some-key" }
```

Of if you need to create and bind multiple NOIDs at once:

```json
{ "bindings": ["some-key","some-other-key"] }
```

To retrieve the NOID attached to the binding, use:

```
GET /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/bind/test
```
