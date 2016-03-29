# JSON-RPC API

```
POST https://server-name/api
```

```json
{
    "method" : "called method",
    "params" : ["method arguments list"],
    "id" : "client token"
}
```
## Методы
Авторизация:
```
user_authorize(login, password) -> token : user token
```

Список содержимого директории:
```
path_list(path) -> {type: dir/file/link, name: item name}
```

Выгрузка алгоритма:
```
path_fetch(path) -> {name, input_spec, output_spec, source}
```

Исполнение:
```
path_exec(path, args) -> result
```

Создание:
```
path_create(path) -> result
```

Перемещение:
```
path_move(source, dest) -> result
```

Изменение:
```
path_edit(path, alg) -> result
```

Удаление:
```
path_remove(path) -> result
```
## Коды ошибок

Невалидный токен (1)

