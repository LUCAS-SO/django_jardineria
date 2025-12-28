# Django Jardineria

Una aplicación web construida con Django para el seguimiento y gestión de trabajos de jardinería. Permite registrar trabajos con fechas, ubicaciones, duraciones, descripciones, etiquetas y fotos antes/después.

## Características

- **Gestión de Trabajos**: Registra trabajos con fecha, ubicación (Delegación, Farmacia, Óptica, Otro), duración en minutos y descripción opcional.
- **Etiquetas**: Asocia etiquetas a los trabajos para una mejor organización.
- **Fotos**: Sube fotos antes y después de cada trabajo, almacenadas en Cloudinary.
- **Vista de Lista**: Muestra una lista paginada de trabajos con totales mensuales.
- **Vista de Detalle**: Muestra detalles de un trabajo específico, incluyendo fotos.
- **Exportación**: Exporta los trabajos a Excel (.xlsx) o PDF con resúmenes mensuales y totales.
- **Rate Limiting**: Limita las solicitudes para prevenir abuso.
- **Middleware Personalizado**: Incluye anti-bot, bloqueo de IP y rate limiting.
- **Almacenamiento en la Nube**: Usa Cloudinary para el almacenamiento de imágenes.

## Tecnologías Utilizadas

- **Django 5.2.9**: Framework web principal.
- **Cloudinary**: Para almacenamiento y gestión de imágenes.
- **ReportLab**: Para generación de PDFs.
- **OpenPyXL**: Para exportación a Excel.
- **PostgreSQL** (en producción) / **SQLite** (en desarrollo).
- **Gunicorn**: Servidor WSGI para despliegue.
- **WhiteNoise**: Para servir archivos estáticos en producción.

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip
- Git

### Pasos de Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/LUCAS-SO/django_jardineria.git
   cd django_jardineria
   ```

2. **Crea un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**:
   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   SECRET_KEY=tu_clave_secreta_aqui
   DEBUG=True
   CLOUDINARY_CLOUD_NAME=tu_cloud_name
   CLOUDINARY_API_KEY=tu_api_key
   CLOUDINARY_API_SECRET=tu_api_secret
   DATABASE_URL=sqlite:///db.sqlite3  # O URL de PostgreSQL para producción
   ```

5. **Ejecuta las migraciones**:
   ```bash
   cd src
   python manage.py migrate
   ```

6. **Crea un superusuario** (opcional, para acceder al admin):
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecuta el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```
   Accede a la aplicación en `http://127.0.0.1:8000/`.

## Uso

- **Página Principal**: Lista de trabajos con paginación y totales mensuales.
- **Detalle de Trabajo**: Haz clic en un trabajo para ver detalles, fotos y duración formateada.
- **Exportación**: Usa los enlaces en la página de lista para descargar datos en Excel o PDF.
- **Administración**: Accede a `/admin/` con credenciales de superusuario para gestionar trabajos, fotos y etiquetas.

## Despliegue

La aplicación está configurada para despliegue en plataformas como Heroku o Render.

- **Procfile**: Define el comando para ejecutar la aplicación con Gunicorn.
- **WhiteNoise**: Sirve archivos estáticos en producción.
- **Database**: Usa `dj-database-url` para configurar la base de datos desde una variable de entorno.

Para desplegar:
1. Configura las variables de entorno en tu plataforma de despliegue.
2. Ejecuta `python manage.py collectstatic` para recopilar archivos estáticos.
3. Despliega usando el Procfile.

## Estructura del Proyecto

```
django_jardineria/
├── Procfile
├── requirements.txt
├── README.md
└── src/
    ├── db.sqlite3
    ├── manage.py
    ├── jardineria_app/
    │   ├── settings.py
    │   ├── urls.py
    │   └── ...
    ├── jobs/
    │   ├── models.py
    │   ├── views.py
    │   ├── middleware/
    │   └── ...
    ├── media/
    ├── static/
    └── templates/
```

## Contribución

1. Haz un fork del proyecto.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Haz commit de tus cambios (`git commit -am 'Agrega nueva funcionalidad'`).
4. Push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT.

## Autor

Lucas Soria
</content>