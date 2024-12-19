# TODO List Application

Esta aplicación es un sistema de gestión de tareas y proyectos simples (TODO List) que permite a los usuarios:

- Crear, actualizar y eliminar proyectos (Todos).
- Gestionar tareas asociadas a cada proyecto.
- Interactuar a través de una interfaz web intuitiva con Bootstrap y JavaScript.

## Funcionalidades principales

- **Gestión de Proyectos (Todos):**
  - Crear un nuevo proyecto.
  - Ver los detalles de un proyecto y las tareas asociadas.
  - Eliminar un proyecto.

- **Gestión de Tareas:**
  - Crear, editar y eliminar tareas dentro de un proyecto específico.

- **Interfaz de usuario:**
  - Basada en plantillas HTML y estilizada con Bootstrap.
  - Respuesta interactiva utilizando jQuery y SweetAlert para notificaciones.

## Requisitos

- Docker y Docker Compose instalados en tu sistema.

## Configuración inicial

1. Asegúrate de tener los archivos necesarios:
   - `Dockerfile`: Define cómo construir la imagen del contenedor.
   - `docker-compose.yml`: Configura los servicios de la aplicación.
   - Código fuente (`main.py`, plantillas HTML).

2. **Base de datos SQLite**:
   - La base de datos se inicializa automáticamente al arrancar el contenedor si no existe.

## Instrucciones para levantar el servicio

1. **Clona el repositorio** (si aún no lo has hecho):

   ```bash
   git clone <URL-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. **Levanta el contenedor con Docker Compose**:

   ```bash
   docker-compose up --build
   ```

3. Accede a la aplicación en tu navegador en:

   ```
   http://localhost:5000
   ```

## Archivos principales

- **`main.py`**: Contiene la lógica del servidor y las rutas para la API REST de la aplicación.
- **`templates/`**: Directorio con las plantillas HTML de la interfaz.
- **`Dockerfile`**: Archivo de configuración para construir la imagen Docker.
- **`docker-compose.yml`**: Configuración para el entorno de Docker Compose.

## Estructura del proyecto

```
.
├── Dockerfile
├── docker-compose.yml
├── main.py
├── templates/
│   ├── index.html.j2
│   ├── todo_detail.html.j2
└── README.md
```

## Características adicionales

- **Recuperación automática de datos iniciales**: 
  - Los datos iniciales se cargan desde un servicio externo para poblar ejemplos en la base de datos.
- **Soporte de errores**:
  - Manejo robusto de errores con mensajes JSON de respuesta.

¡Disfruta gestionando tus tareas con esta aplicación!
