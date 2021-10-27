# Deployment


# Docker


## Nginx


## Odoo

## Postgres


Agregar usuario postgres `odoo`

Ingresamos con usuario postgres


### Creamos usuario

```bash
createuser -s odoo
```
### Creamos cambiar passord

Ingresamos al psql

```bash
psql
```

```sql
ALTER USER odoo WITH PASSWORD 'odoo';
\q
```



## Permisos de carpeta

```bash
sudo chmod -R 777 odoo
```


## Solo para simular dominio

```bash
sudo nano /etc/hosts
```

Agregamos

```
127.0.0.1 odoo14.fullstack
```



