# duohnson — Catálogo virtual con carrito de compras

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 6.0">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/WhiteNoise-6.5-lightgrey?style=for-the-badge" alt="WhiteNoise">
</p>

---

Plataforma web desarrollada en Django que funciona como catálogo digital para un emprendimiento de accesorios. El sistema permite explorar productos, gestionar un carrito de compras por usuario y generar pedidos directos vía WhatsApp. Pensado para negocios pequeños que necesitan presencia online sin depender de pasarelas de pago.

---

## Tabla de contenido

- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Funcionalidades](#funcionalidades)
- [Stack técnico](#stack-técnico)
- [Estructura de directorios](#estructura-de-directorios)
- [Requisitos previos](#requisitos-previos)
- [Instalación y configuración](#instalación-y-configuración)
- [Variables de entorno](#variables-de-entorno)
- [Modelo de datos](#modelo-de-datos)
- [Middleware personalizado](#middleware-personalizado)
- [Endpoints principales](#endpoints-principales)
- [Despliegue en producción](#despliegue-en-producción)
- [Capturas](#capturas)
- [Licencia](#licencia)

---

## Arquitectura del proyecto

El proyecto sigue una arquitectura modular basada en Django apps, donde cada dominio del negocio está encapsulado en su propia aplicación:

```
proyecto/            → Configuración central (settings, urls, middleware, wsgi)
home/                → Página principal y contacto
tienda/              → Catálogo, detalle de producto, carrito de compras
buscador/            → Motor de búsqueda por texto con paginación
usuarios/            → Registro, login, logout, perfil con foto
```

La comunicación entre apps se mantiene desacoplada: `home` consulta productos de `tienda` solo para mostrar ofertas en la landing, y `buscador` filtra contra el modelo `Producto` sin dependencias circulares.

---

## Funcionalidades

| Módulo | Descripción |
|---|---|
| **Catálogo** | Listado paginado de productos con múltiples imágenes por producto. Soporte de carrusel en la vista de detalle. |
| **Carrito** | Carrito persistente por usuario autenticado. Agregar, eliminar productos y ver el total en tiempo real. |
| **Pedido por WhatsApp** | Al confirmar el carrito, se genera automáticamente un mensaje con el detalle completo del pedido y se abre WhatsApp con el texto prellenado. |
| **Búsqueda** | Filtrado por nombre y descripción con consultas `Q` de Django. Resultados paginados. |
| **Autenticación** | Registro con validación de contraseñas, login/logout, y perfil con carga de foto de perfil. |
| **Ofertas** | Los productos marcados como oferta se muestran destacados en la página principal. |
| **Perfil de usuario** | Foto de perfil visible en la navbar. Signals de Django crean el perfil automáticamente al registrarse. |
| **Panel de admin** | Gestión completa de productos e imágenes desde el admin de Django con inlines. |

---

## Stack técnico

| Capa | Tecnología |
|---|---|
| Backend | Django 6.0 (Python 3.12+) |
| Base de datos | MySQL 8.0 |
| Servidor WSGI (producción) | Waitress |
| Archivos estáticos | WhiteNoise con compresión |
| Frontend | HTML5, CSS3 vanilla, JavaScript vanilla |
| Gestión de imágenes | Pillow |
| Variables de entorno | python-dotenv |

---

## Estructura de directorios

```
├── manage.py                  # Utilidad CLI de Django
├── run.py                     # Servidor de producción (Waitress + WhiteNoise)
├── requirements.txt           # Dependencias del proyecto
├── .env.template              # Plantilla de variables de entorno
├── .gitignore                 # Archivos excluidos de git
│
├── proyecto/                  # Configuración central
│   ├── settings.py            # Settings con variables de entorno y MySQL
│   ├── urls.py                # Rutas raíz del proyecto
│   ├── middleware.py          # Middleware de seguridad, timing y rate limiting
│   ├── wsgi.py
│   └── asgi.py
│
├── home/                      # App: landing y contacto
│   ├── views.py
│   ├── urls.py
│   └── templates/home/
│       ├── index.html         # Página principal con ofertas
│       └── contacto.html      # Información del negocio
│
├── tienda/                    # App: catálogo y carrito
│   ├── models.py              # Producto, ProductImage, Cart, CartItem
│   ├── views.py               # CRUD del carrito, catálogo, detalle
│   ├── admin.py               # Admin con imágenes inline
│   ├── context_processors.py  # Contador de carrito global
│   ├── urls.py
│   └── templates/home/
│       ├── catalogo.html      # Grilla de productos paginada
│       ├── detalle_producto.html  # Detalle con carrusel de imágenes
│       └── cart.html           # Vista del carrito
│
├── buscador/                  # App: búsqueda de productos
│   ├── views.py               # Búsqueda con Q lookups
│   └── templates/home/
│       └── search.html        # Resultados de búsqueda
│
├── usuarios/                  # App: autenticación y perfiles
│   ├── models.py              # Profile (foto de perfil)
│   ├── views.py               # Registro, login, logout, perfil
│   ├── signals.py             # Auto-creación de perfil
│   └── templates/usuarios/
│       ├── login.html
│       ├── registro.html
│       └── perfil.html
│
├── templates/
│   └── base.html              # Template base con navbar, footer, búsqueda
│
├── static/
│   ├── css/
│   │   ├── style.css          # Estilos principales (responsive)
│   │   └── snow.css           # Efecto decorativo de nieve
│   ├── js/
│   │   └── snow.js            # Generador de copos de nieve
│   └── img/                   # Imágenes estáticas
│
└── media/                     # Uploads de usuarios (gitignored)
    ├── productos/
    └── perfiles/
```

---

## Requisitos previos

- **Python** 3.12 o superior
- **MySQL** 8.0 o superior (con una base de datos creada llamada `base`)
- **pip** actualizado
- **Git**

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/duohnson/virtual-catalog.git
cd tu-repositorio
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos en MySQL

```sql
CREATE DATABASE base CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar variables de entorno

```bash
cp .env.template .env
```

Editar el archivo `.env` con los datos de conexión a la base de datos y la clave secreta. Para generar una clave segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. Recopilar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 9. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a `http://127.0.0.1:8000/` para ver el sitio.

Para producción, usar el servidor Waitress:

```bash
python run.py
```

---

## Variables de entorno

| Variable | Descripción | Ejemplo |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Django | `d1$k3y...` |
| `DEBUG` | Modo debug (`True` / `False`) | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos separados por coma | `localhost,127.0.0.1` |
| `DB_NAME` | Nombre de la base de datos | `base` |
| `DB_USER` | Usuario de MySQL | `root` |
| `DB_PASSWORD` | Contraseña de MySQL | `mi_password` |
| `DB_HOST` | Host de la base de datos | `localhost` |
| `DB_PORT` | Puerto de MySQL | `3306` |

---

## Modelo de datos

```
┌──────────────┐       ┌──────────────────┐
│   Producto   │       │   ProductImage   │
├──────────────┤       ├──────────────────┤
│ id           │──┐    │ id               │
│ nombre       │  │    │ producto (FK)    │──┐
│ precio       │  └───>│ imagen           │  │
│ descripcion  │       └──────────────────┘  │
│ is_oferta    │                              │
└──────────────┘                              │
       │                                      │
       │ (referenciado por CartItem)           │
       ▼                                      │
┌──────────────┐       ┌──────────────────┐   │
│   CartItem   │       │      Cart        │   │
├──────────────┤       ├──────────────────┤   │
│ id           │       │ id               │   │
│ cart (FK)    │──────>│ user (1:1 User)  │   │
│ producto(FK) │       │ created_at       │   │
│ quantity     │       └──────────────────┘   │
└──────────────┘                              │
                                              │
┌──────────────┐       ┌──────────────────┐   │
│    User      │       │    Profile       │   │
│  (Django)    │──────>│ user (1:1)       │   │
│              │       │ foto_perfil      │   │
└──────────────┘       └──────────────────┘   │
```

Cada producto puede tener múltiples imágenes a través de `ProductImage`. El carrito (`Cart`) es uno por usuario, y cada `CartItem` vincula un producto con su cantidad. El `Profile` extiende al modelo `User` de Django con una foto de perfil, creándose automáticamente mediante signals.

---

## Middleware personalizado

Implementé tres middleware ubicados en `proyecto/middleware.py`:

### SecurityHeadersMiddleware

Agrega cabeceras de seguridad HTTP a cada respuesta:
- `X-Content-Type-Options: nosniff` — previene MIME sniffing
- `X-XSS-Protection: 1; mode=block` — protección contra XSS reflejado
- `Referrer-Policy: strict-origin-when-cross-origin` — controla qué información del referrer se envía
- `Permissions-Policy` — deshabilita acceso a geolocalización, micrófono y cámara
- `Strict-Transport-Security` — fuerza HTTPS en producción

### RequestTimingMiddleware

Mide el tiempo de procesamiento de cada petición. Si un request tarda más de 1 segundo, registra un warning en los logs. Útil para identificar endpoints con problemas de rendimiento.

### RateLimitMiddleware

Limitador de peticiones por IP en memoria. Restringe a 100 requests por minuto por IP cuando `DEBUG=False`. Ante exceso, responde con HTTP 429. Los parámetros son configurables desde `settings.py` con `RATE_LIMIT_MAX_REQUESTS` y `RATE_LIMIT_WINDOW`.

---

## Endpoints principales

| Método | Ruta | Vista | Descripción |
|---|---|---|---|
| GET | `/` | `home.index` | Landing con ofertas |
| GET | `/contacto/` | `home.contacto` | Información de contacto |
| GET | `/catalogo/` | `tienda.catalogo` | Catálogo paginado |
| GET | `/catalogo/producto/<id>/` | `tienda.detalle_producto` | Detalle con carrusel |
| POST | `/catalogo/producto/<id>/add_to_cart/` | `tienda.add_to_cart` | Agregar al carrito |
| GET | `/catalogo/cart/` | `tienda.view_cart` | Ver carrito |
| GET | `/catalogo/cart/remove/<id>/` | `tienda.remove_from_cart` | Eliminar del carrito |
| GET | `/buscar/?q=texto` | `buscador.buscar` | Búsqueda de productos |
| GET/POST | `/usuarios/registro/` | `usuarios.registro_view` | Registro |
| GET/POST | `/usuarios/login/` | `usuarios.login_view` | Login |
| GET | `/usuarios/logout/` | `usuarios.logout_view` | Logout |
| GET/POST | `/usuarios/perfil/` | `usuarios.perfil_view` | Perfil de usuario |
| — | `/admin/` | Admin de Django | Panel de administración |

---

## Despliegue en producción

### Configuración mínima

1. Establecer `DEBUG=False` en `.env`
2. Configurar `ALLOWED_HOSTS` con el dominio real
3. Generar una `SECRET_KEY` segura y distinta a la de desarrollo
4. Ejecutar `python manage.py collectstatic --noinput`

### Seguridad automática en producción

Cuando `DEBUG=False`, el proyecto activa automáticamente:

- Redirección forzada a HTTPS (`SECURE_SSL_REDIRECT`)
- Cookies de sesión y CSRF marcadas como seguras
- HSTS con preload habilitado (1 año)
- `X-Frame-Options: DENY`
- Rate limiting activo (100 req/min por IP)

### Servidor recomendado

El archivo `run.py` levanta Waitress con WhiteNoise integrado, listo para producción en Windows o Linux sin necesidad de Nginx para archivos estáticos:

```bash
python run.py
```

Para entornos Linux con mayor carga, se puede reemplazar Waitress por Gunicorn y usar Nginx como reverse proxy.

---

## Capturas

A continuación, se muestran algunas capturas de pantalla del sitio:

### Página principal
![Página principal](capturas/Captura1.png)

### Catálogo de productos
![Catálogo de productos](capturas/Captura2.png)

### Inicio de sesión
![Iniciar Sesión](capturas/Captura3.png)

---

