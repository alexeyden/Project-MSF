# JSON-RPC API

http://www.jsonrpc.org/specification

Обращение к серверу:
```
POST https://server-name/api
```

Вызов метода на сервере:
```json
{
    "method" : "called method",
    "params" : ["method arguments list"],
    "id" : "client token"
}
```

Формат ответа:
```json
{
    "result": "sdsd",
    "error": null,
    "id": "client token"
}
```

## Методы#
### Авторизация

```
user_authorize(login, password) -> token
```

`token` - временный токен (строка)

### Список содержимого директории

```
path_list(path) -> paths
```

`paths` - список объектов FileInfo

FileInfo:
```json
{
    "name" : name
    "path" : path
    "owner" : owner
    "shared" : shared
    "is_directory" : is_directory
    "can_write" :  can_write
    "can_read" : can_read
}
```

### Выгрузка алгоритма:

```
path_fetch(path) -> algorithm
```

### Исполнение:

```
path_exec(path, args) -> result
```

### Создание:

```
path_create(path) -> result
```

### Перемещение:

```
path_move(source, dest) -> result
```

### Изменение:
```
path_edit(path, alg) -> result
```

### Удаление:
```
path_remove(path) -> result
```
## Ошибки

Формат:
```json
{
    "code": 1,
    "message": "some message",
    "data": "additional data"
}
```

### Коды ошибок

**1**. Ошибка авторизации (неверный логин пароль, неверный токен

