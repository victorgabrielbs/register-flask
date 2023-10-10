See the .env.example

```sql
create database maindatabase;

use maindatabase;

create table py_user (
    id char(36) primary key,
    name varchar(255) not null,
    email varchar(255) not null,
    password varchar(255) not null
);
```

```bash

pip3 install -r requirements.txt

flask --app server run #dev
```
