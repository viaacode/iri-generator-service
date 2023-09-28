# NOID generator service

This application runs a Web service that dispenses NOIDs or IRIs to applications.
It can create multiple independent minters that are capable to mint and persist NOIDs. Minters can also bind minted NOIDs to a string for later retrieval. 
The NOID generator uses [noid](https://pypi.org/project/noid/) for minting NOIDs , and PostgreSQL for persisting all minter configurations, the minted noids, and their bindings.

## API

### Creating a new minter

You can create a new minter by executing `POST` to `/api/v1/minters/`. 
The configuration for the minter can be supplied with a JSON payload, like below (these are the default values):
```
{
    "scheme": "",
    "naa": "",
    "template": "zedededek",
}
```

This will return something like 

```
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

The minter is now available at `/api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/`

### Creating one or more NOIDs

Once you have created a minter, you can use it to mint new noids. 
To create one or more new NOIDs, run a `POST` to `/api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/` and it will a new NOID every time.
For example:
```

```

In case you need multiple noids, pass the count parameter in the body:

```
{
    count: 3
}
```

You can retrieve the metadata of this NOID by

```
GET /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/00
```

### Binding a key to a NOID

You can also bind any string to a NOID in case you need to reproduce it.
For example, binding the NOID `00` to `key`
```
PUT /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/00/binding/key
```
You can retrieve the binding by doing

```
GET /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/00/binding/
```

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
DELETE /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/noids/00/binding/
```



You can also create and bind nodes at the same time. 

```
POST /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/bind/
```

```
{ bindings: "some-key" }
```

Of if you need to create and bind multiple NOIDs at once:
```
{ bindings: ["some-key","some-other-key"] }
```


```
GET /api/v1/minters/065158d0-5899-7d79-8000-eac0bd0a47c1/bind/test
```


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
