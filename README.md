<p align="center">
  <img src="https://learnx.up.railway.app/static/media/Newwork/logobnex.png" alt="Logo de Nexwork" width="100" />
</p>

<h1 align="center">Nexwork</h1>

<p align="center">
  <img src="https://learnx.up.railway.app/static/media/Newwork/NexWorkApp2.gif" alt="Demo de Nexwork" width="90%">
</p>

<p align="center">
  <a href="#" target="_blank">
    <img src="https://img.shields.io/badge/▶️ Probar Nexwork-Registro-blue?style=for-the-badge&logo=python" alt="Probar Nexwork">
  </a>
  &nbsp;
  <a href="#" target="_blank">
    <img src="https://img.shields.io/badge/ Ver demo-YouTube-red?style=for-the-badge&logo=youtube" alt="Ver demo en YouTube">
  </a>
</p>

**Nexwork** es una red social profesional desarrollada con Django, inspirada en plataformas como LinkedIn, pero con un enfoque más simple, directo y personalizable.

Este proyecto busca ofrecer un espacio donde los usuarios puedan construir un perfil profesional completo con su experiencia laboral, educación y habilidades, y así postularse a oportunidades laborales publicadas por otros usuarios. Nexwork facilita conexiones profesionales, comunicación en tiempo real y gestión activa del perfil, todo desde una interfaz intuitiva y responsiva.

Este proyecto va más allá de un simple muro de publicaciones. Nexwork es un ecosistema completo de interacción profesional: incluye funcionalidades como historias, solicitudes de amistad, mensajería en tiempo real, y estadísticas graficadas sobre el alcance de las publicaciones. Todo desarrollado con una arquitectura moderna, completamente dinámica, fluida y responsive.

---

## 📑 Índice

<details>
<summary><strong>🎯 Propósito del proyecto</strong></summary>

- [Ir a la sección](#-propósito-del-proyecto)

</details>

<details>
<summary><strong>📌 Distintividad y complejidad</strong></summary>

- [Ir a la sección](#-distintividad-y-complejidad)

</details>

<details>
<summary><strong>⚙️ Tecnologías utilizadas</strong></summary>

- [Ir a la sección](#️-tecnologías-utilizadas)

</details>

<details>
<summary><strong>🚀 Instalación y ejecución</strong></summary>

- [Ir a la sección](#-instalación-y-ejecución)

</details>

<details>
<summary><strong>🔐 Credenciales de acceso</strong></summary>

- [Ir a la sección](#-credenciales-de-acceso)

</details>

<details>
<summary><strong>💼 Cómo funciona Nexwork</strong></summary>

- [Cómo funciona Nexwork](#-cómo-funciona-nexwork)  
  - [👤 Registro de usuarios](#-registro-de-usuarios)  
  - [🖼️ Personalización del perfil](#️-personalización-del-perfil)  
  - [📝 Publicaciones y contenido](#-publicaciones-y-contenido)  
  - [🤝 Conexiones e interacción](#-conexiones-e-interacción)  
  - [🎯 Postulaciones laborales](#-postulaciones-laborales)  
  - [💡 Un espacio para destacar](#-un-espacio-para-destacar)

</details>

<details>
<summary><strong>🧠 Código y organización</strong></summary>

- [Código y organización](#-código-y-organización)  
  - [📦 App principal: NexworkApp](#-app-principal-nexworkapp)  
  - [🎨 Templates](#-templates)  
  - [🖼️ Static files](#️-static-files)  
  - [⚙️ Proyecto base: NexworkProject](#️-proyecto-base-nexworkproject)

</details>

<details>
<summary><strong>📄 Acerca de y licencia</strong></summary>

- [Ir a la sección](#-acerca-de-y-licencia)

</details>

---

## 🎯 Propósito del proyecto

Nexwork surge como proyecto final para el curso [**CS50’s Web Programming with Python and JavaScript**](https://cs50.harvard.edu/web/2020/projects/final/capstone/), integrando todo lo aprendido sobre desarrollo web full-stack, con tecnologías modernas y patrones de diseño eficientes. A diferencia de proyectos básicos, Nexwork propone una solución profesional completa en la que los usuarios no solo crean un perfil, sino que participan activamente en una red viva de interacción profesional, empleabilidad y colaboración.

---

## 📌 Distintividad y complejidad

Nexwork destaca por ofrecer un conjunto de funcionalidades avanzadas y una experiencia de usuario fluida, digna de una aplicación profesional. A continuación se detallan las principales características distintivas:

| Funcionalidad                             | Descripción                                                                                                                                           |
|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🔄 **Frontend dinámico**                  | Interacciones como publicaciones, comentarios, reacciones y solicitudes se actualizan por AJAX sin recargar la página.                              |
| 💬 **Mensajería en tiempo real**         | Comunicación en vivo mediante WebSockets, gestionada con Django Channels.                                                                             |
| 🪧 **Historias y publicaciones**          | Función tipo red social: publicaciones personales y públicas, con sistema de comentarios, likes y posibilidad de compartir.                          |
| 📊 **Estadísticas visuales**             | Cada publicación muestra visualizaciones detalladas por ciudades, etiquetas y vistas, representadas con gráficas interactivas.                       |
| 🤝 **Red de conexiones**                 | Los usuarios pueden enviar solicitudes de amistad, recibir notificaciones dinámicas y formar una red profesional.                                    |
| 👤 **Perfil enriquecido y editable**      | Sección de perfil personalizable con experiencia laboral, estudios, foto de portada, imagen de perfil y datos de contacto.                           |
| 🛠️ **Panel administrativo**             | Panel de control con administración de usuarios, publicaciones, postulaciones y seguimientos, con filtros optimizados.                              |

> Estas funcionalidades convierten a **Nexwork** en una aplicación de alta complejidad, con múltiples módulos interconectados.  
> Requiere dominio técnico tanto del frontend (**AJAX, JS, Chart.js, SweetAlert2**) como del backend (**Django, Channels, WebSockets, SQLite**), y un enfoque UX responsivo adaptado a múltiples dispositivos.

## ⚙️ Tecnologías utilizadas

| Categoría                    | Tecnologías                                   |
|-----------------------------|-----------------------------------------------|
| **Backend**                 | Django 5.0.9, Django Channels                  |
| **Base de datos**           | SQLite                                        |
| **Frontend**                | HTML5, JavaScript (AJAX), Bootstrap 5.3.3, SweetAlert2 |
| **Comunicación en tiempo real** | WebSockets (Django Channels)             |
| **Gráficas**                | Chart.js                                      |
| **Archivos estáticos**      | WhiteNoise                                    |
| **Entorno**                 | Python 3.x, SQLite3                           |


---

## 🚀 Instalación y ejecución

<details>
<summary><strong>1. Clonar el repositorio</strong></summary>

```bash
git clone https://github.com/JJuan777/Nexwork.git
cd Nexwork
```
</details>

<details>
<summary><strong>2. Crear un entorno virtual</strong></summary>

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```
</details>

<details>
<summary><strong>3. Instalar requerimientos</strong></summary>

```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>4. Ejecutar el servidor</strong></summary>

```bash
python manage.py runserver
```

Luego abre tu navegador y entra a:

```
http://127.0.0.1:8000/
```
</details>

---

## 🔐 Credenciales de acceso

Puedes usar las siguientes cuentas para probar la aplicación:

### 👤 Usuario común
- **Usuario:** `jj.uan77`
- **Contraseña:** `p4$$w0r321`

### 🛠️ Usuario administrador
- **Usuario:** `jj.uan77`
- **Contraseña:** `p4$$w0r321`
- **Panel admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---
## 💼 Cómo funciona Nexwork

Nexwork es una plataforma profesional que permite a los usuarios crear perfiles, compartir contenido, buscar oportunidades laborales y conectar con otros profesionales o empresas.

### 👤 Registro de usuarios

Cualquier persona puede registrarse en [http://127.0.0.1:8000/registro/](http://127.0.0.1:8000/registro/), donde podrá elegir uno de los siguientes roles:

- **Usuario profesional:** Ideal para personas que buscan oportunidades laborales, quieren construir y compartir un perfil profesional completo con su experiencia académica, laboral y habilidades destacadas.
- **Empresa o reclutador:** Diseñado para crear ofertas de trabajo y gestionar postulaciones. Perfecto para empresas, HR managers o reclutadores que buscan talento.

Al completar el registro, el sistema redirige automáticamente al usuario para que alimente su perfil con información académica y laboral relevante. Cuanta más información incluya, más atractivo será su perfil para otros.

### 🖼️ Personalización del perfil

- Agrega tu **foto de perfil** y un **banner profesional**.
- Añade **experiencia laboral**, **formación académica**, **habilidades**, y más.
- Comparte tu perfil con otros, como si fuera tu currículum en línea.

### 📝 Publicaciones y contenido

Los usuarios pueden:
- Crear **publicaciones profesionales** para compartir ideas, logros o actualizaciones.
- **Subir historias** efímeras tipo red social.
- **Compartir publicaciones** de otros usuarios con su red.
- **Comentar y reaccionar** a contenido publicado por otros.

### 🤝 Conexiones e interacción

Nexwork fomenta la interacción entre usuarios mediante:
- Solicitudes de amistad y creación de una red profesional.
- **Mensajes en tiempo real** vía WebSockets para una comunicación fluida.
- Notificaciones dinámicas sobre conexiones, postulaciones y más.

### 🎯 Postulaciones laborales

- Los usuarios con perfil profesional pueden **postularse** fácilmente a los trabajos publicados.
- Las empresas reciben **tarjetas de presentación** con la información del postulante.
- Las vacantes pueden incluir estadísticas sobre **visualización, ubicación y etiquetas** destacadas.

### 💡 Un espacio para destacar

La plataforma está diseñada para ser una herramienta flexible: puedes usarla como portafolio profesional, como red de contactos laborales, o como sistema de búsqueda de talento. Tú decides cómo aprovecharla.

---

🚀 **Explora, crea y conecta. Nexwork es el siguiente paso en tu vida profesional digital.**


---
## 🧠 Código y organización

El proyecto **Nexwork** está organizado en una arquitectura modular, que separa de manera clara la lógica de negocio, las vistas, los recursos estáticos y las plantillas HTML.

### Estructura general

Los directorios principales del proyecto son:

- **NexworkApp/**: contiene toda la lógica de la aplicación, vistas, modelos, formularios, templatetags y migraciones.
- **NexworkProject/**: carpeta raíz del proyecto Django que contiene los archivos de configuración (`settings.py`, `urls.py`, etc.).
- **static/**: contiene todos los recursos estáticos como hojas de estilo, scripts JS, imágenes.
- **templates/**: almacena las plantillas HTML organizadas por módulo o funcionalidad (`auth/`, `layouts/`, etc.).

---

### 📦 App principal: NexworkApp

La aplicación `NexworkApp` concentra toda la funcionalidad del sistema:

- `views.py`: contiene la lógica de cada sección (perfil, publicaciones, historias, trabajos, solicitudes, etc.).
- `models.py`: define todos los modelos de la base de datos (usuarios, trabajos, postulaciones, mensajes, etc.).
- `forms.py`: formularios personalizados utilizados en el registro, publicaciones, postulaciones y demás.
- `templatetags/`: filtros personalizados de Django usados en plantillas (por ejemplo, formateo de fechas o extracción de nombres).
- `migrations/`: contiene las migraciones generadas por Django para crear y modificar la base de datos.

---

### 🎨 Templates

Las vistas HTML están organizadas en:

- `templates/Nexwork/layouts/`: estructura base de la interfaz (barra de navegación, layout general).
- `templates/Nexwork/auth/`: vistas de autenticación como login y registro.
- Otras vistas están divididas según módulos específicos (perfil, publicaciones, historias, estadísticas, etc.).

---

### 🖼️ Static files

Los archivos estáticos están en:

- `static/css/`, `static/js/`, `static/images/`: contienen los estilos, scripts personalizados e imágenes del proyecto.
- `static/bootstrap-5.3.3/`: versión local de Bootstrap utilizada en la UI.
- `static/js/Nexwork/auth/`: scripts específicos para login, registro y validaciones.
- `static/media/`: carpeta reservada para archivos multimedia (imágenes de perfil, banners, etc.).

---

### ⚙️ Proyecto base: NexworkProject

Contiene los archivos base de configuración de Django:

- `settings.py`: configuración principal del proyecto.
- `urls.py`: mapeo de rutas y vistas.
- `asgi.py / wsgi.py`: punto de entrada para servidores ASGI/WSGI.

---

## 📄 Acerca de y licencia

Este proyecto fue desarrollado originalmente en 2025 como proyecto final del curso [**CS50’s Web Programming with Python and JavaScript**](https://cs50.harvard.edu/web/2020/projects/final/capstone/) de HarvardX.

La versión principal actual se encuentra en la rama `main`, y ha sido mejorada con nuevas funcionalidades desde su entrega inicial: mensajes en tiempo real, estadísticas visuales, sistema de postulaciones, historias y un diseño completamente responsivo.

Este es un proyecto personal, de código abierto, distribuido bajo la **Licencia MIT**. Puedes usarlo, estudiarlo, modificarlo o distribuirlo libremente bajo los términos de dicha licencia.

**Nexwork** se proporciona "tal cual", sin garantías de ningún tipo. El autor no se hace responsable de ningún daño, pérdida de datos o inconveniente causado por el uso del software.

Si te gustó este proyecto, ¡considera motivar al desarrollador dejando una ⭐ en [GitHub](https://github.com/JJuan777/Nexwork)!
