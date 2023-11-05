# odoo-14

### Working with Docker

Prerequisites:

- git
- docker
- docker-compose

1. Clone this project

    ```bash
    git clone git@github.com:marfandy/odoo-14.git
    ```

2. Run App
    ```bash
    docker compose up -d --build
    ```

### Run Test
```bash
docker compose up -d --build
```

```bash
docker compose stop 
```

```bash
docker compose run web --test-enable --stop-after-init -d {db_name} -i {addons}

docker compose run web --test-enable --stop-after-init -d odoo -i _material
```