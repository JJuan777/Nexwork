<p align="center">
  <img src="https://learnx.up.railway.app/static/media/Newwork/logobnex.png" alt="Logo de Nexwork" width="100" />
</p>

<h1 align="center">Nexwork</h1>

<p align="center">
  <img src="https://learnx.up.railway.app/static/media/Newwork/NexWorkApp2.gif" alt="Nexwork Demo" width="90%">
</p>

<p align="center">
  <a href="https://nexwork-app.up.railway.app/login" target="_blank">
    <img src="https://img.shields.io/badge/▶️ Try Nexwork-Register-blue?style=for-the-badge&logo=python" alt="Try Nexwork">
  </a>
  &nbsp;
  <a href="https://youtu.be/4KzoLzLYo2I?si=BWUPDV-vyRayag3F" target="_blank">
    <img src="https://img.shields.io/badge/ Watch demo-YouTube-red?style=for-the-badge&logo=youtube" alt="Watch demo on YouTube">
  </a>
</p>

**Nexwork**  is a professional social network built with Django, inspired by platforms like LinkedIn, but with a simpler, more direct, and customizable approach.

This project aims to provide a space where users can build a complete professional profile including work experience, education, and skills, and apply to job opportunities posted by other users. Nexwork enables professional connections, real-time communication, and active profile management — all from an intuitive and responsive interface.

This project goes beyond a simple post feed. Nexwork is a complete ecosystem of professional interaction: it includes features such as stories, friend requests, real-time messaging, and visual statistics to measure the reach of posts. All developed with a modern architecture that is fully dynamic, smooth, and responsive.

---

## 📑 Table of Contents

<details>
<summary><strong>🎯 Project Purpose</strong></summary>

- [Go to section](#-project-purpose)

</details>

<details>
<summary><strong>📌 Distinctiveness and Complexity</strong></summary>

- [Go to section](#-uniqueness-and-complexity)

</details>

<details>
<summary><strong>⚙️ Technologies Used</strong></summary>

- [Go to section](#-technologies-used)

</details>

<details>
<summary><strong>🚀 Installation & Execution</strong></summary>

- [Go to section](#-installation--execution)

</details>

<details>
<summary><strong>🔐 Access Credentials</strong></summary>

- [Go to section](#-access-credentials)

</details>

<details>
<summary><strong>💼 How Nexwork Works</strong></summary>

- [How Nexwork Works](#-how-nexwork-works)  
  - [👤 User Registration](#-user-registration)  
  - [🖼️ Profile Customization](#️-profile-customization)  
  - [📝 Posts and Content](#-posts-and-content)  
  - [🤝 Connections and Interaction](#-connections-and-interaction)  
  - [🎯 Job Applications](#-job-applications)  
  - [💡 A Space to Stand Out](#-a-space-to-stand-out)

</details>

<details>
<summary><strong>🧠 Code and Structure</strong></summary>

- [Code and Structure](#-code-and-structure)  
  - [📦 Main App: NexworkApp](#-main-app-nexworkapp)  
  - [🎨 Templates](#-templates)  
  - [🖼️ Static Files](#️-static-files)  
  - [⚙️ Project Base: NexworkProject](#️-project-base-nexworkproject)

</details>

<details>
<summary><strong>📄 About & License</strong></summary>

- [Go to section](#-about--license)

</details>

<details>
<summary><strong>📦 Railway Deployment</strong></summary>

- [Railway Deployment](#deploy-railway)

</details>

---

## 🎯 Project Purpose

Nexwork was created as the final project for the course [**CS50’s Web Programming with Python and JavaScript**](https://cs50.harvard.edu/web/2020/projects/final/capstone/), integrating everything learned about full-stack web development using modern technologies and efficient design patterns. 

Unlike basic projects, Nexwork offers a complete professional solution where users not only build a profile but also actively engage in a dynamic network of professional interaction, employment opportunities, and collaboration.

---

## 📌 Distinctiveness and Complexity

Nexwork stands out by offering a set of advanced features and a smooth user experience, worthy of a professional-grade application. Below are the main distinctive features:

| Feature                                 | Description                                                                                                                                           |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🔄 **Dynamic Frontend**                | Interactions such as posts, comments, reactions, and requests are updated via AJAX without reloading the page.                                       |
| 💬 **Real-Time Messaging**             | Live communication through WebSockets, managed using Django Channels.                                                                                |
| 🪧 **Stories and Posts**               | Social network-style functionality: users can create personal or public posts, with support for comments, likes, and sharing.                        |
| 📊 **Visual Statistics**               | Each post shows detailed view statistics by city, tags, and total reach, displayed using interactive charts.                                         |
| 🤝 **Connection Network**              | Users can send friend requests, receive real-time notifications, and build a professional network.                                                   |
| 👤 **Rich and Editable Profiles**      | Customizable profiles with work experience, education, cover photo, profile image, and contact information.                                          |
| 🛠️ **Admin Panel**                    | Management panel for users, posts, job applications, and follow-ups, with optimized filtering tools.                                                 |

> These features make **Nexwork** a high-complexity application, with multiple interconnected modules.  
> It requires technical proficiency in both frontend (**AJAX, JS, Chart.js, SweetAlert2**) and backend (**Django, Channels, WebSockets, SQLite**), as well as a responsive UX approach suitable for all devices.

## ⚙️ Technologies Used

| Category                    | Technologies                                   |
|----------------------------|------------------------------------------------|
| **Backend**                | Django 5.0.9, Django Channels                  |
| **Database**               | SQLite                                         |
| **Frontend**               | HTML5, JavaScript (AJAX), Bootstrap 5.3.3, SweetAlert2 |
| **Real-Time Communication**| WebSockets (Django Channels)                   |
| **Charts & Graphs**        | Chart.js                                       |
| **Static Files**           | WhiteNoise                                     |
| **Environment**            | Python 3.x, SQLite3                            |

---

## 🚀 Installation & Execution

<details>
<summary><strong>1. Clone the repository</strong></summary>

```bash
git clone https://github.com/JJuan777/Nexwork.git
cd Nexwork
```
</details>

<details>
<summary><strong>2. Create a virtual environment</strong></summary>

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
</details>

<details>
<summary><strong>3. Install requirements</strong></summary>

```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>4. Run the server</strong></summary>

```bash
python manage.py runserver
```

Then open your browser and go to:

```
http://127.0.0.1:8000/
```
</details>

---

## 🔐 Access Credentials

You can use the following accounts to test the application:

### 👤 Regular User
- **Username:** `jj.uan77`
- **Password:** `p4$$w0r321`

### 🛠️ Administrator User
- **Username:** `jj.uan77`
- **Password:** `p4$$w0r321`
- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 💼 How Nexwork Works

Nexwork is a professional platform that allows users to create profiles, share content, search for job opportunities, and connect with other professionals or companies.

### 👤 User Registration

Anyone can register at [http://127.0.0.1:8000/registro/](http://127.0.0.1:8000/registro/), where they can choose from the following roles:

- **Professional User:** Ideal for individuals seeking job opportunities and looking to build and share a complete professional profile including academic background, work experience, and skills.
- **Company or Recruiter:** Designed to create job postings and manage applications. Perfect for companies, HR managers, or recruiters searching for talent.

After registration, users are automatically redirected to complete their profile with relevant academic and professional information. The more complete the profile, the more appealing it becomes to others.

### 🖼️ Profile Customization

- Add your **profile picture** and a **professional banner**.
- Include your **work experience**, **education**, **skills**, and more.
- Share your profile with others — like an online résumé.

### 📝 Posts and Content

Users can:
- Create **professional posts** to share ideas, achievements, or updates.
- Upload **ephemeral stories** similar to social media.
- **Share other users' posts** with their own network.
- **Comment and react** to shared content.

### 🤝 Connections and Interaction

Nexwork promotes user interaction through:
- Friend requests and the creation of a professional network.
- **Real-time messaging** via WebSockets for seamless communication.
- Dynamic notifications about connections, job applications, and more.

### 🎯 Job Applications

- Users with a professional profile can **apply** directly to job postings.
- Companies receive **presentation cards** with applicant information.
- Job posts may include **view statistics**, **location insights**, and **highlighted tags**.

### 💡 A Space to Stand Out

The platform is designed to be flexible: use it as a professional portfolio, a networking tool, or a talent search system. You decide how to make the most of it.

---

🚀 **Explore, create, and connect. Nexwork is the next step in your digital professional journey.**

---

## 🧠 Code and Structure

The **Nexwork** project is organized using a modular architecture that clearly separates business logic, views, static assets, and HTML templates.

### General Structure

The main directories in the project are:

- **NexworkApp/**: Contains all application logic, including views, models, forms, template tags, and migrations.
- **NexworkProject/**: The root Django project folder, containing configuration files (`settings.py`, `urls.py`, etc.).
- **static/**: Stores all static assets such as stylesheets, JavaScript files, and images.
- **templates/**: Contains HTML templates, organized by module or feature (`auth/`, `layouts/`, etc.).

---

### 📦 Main App: NexworkApp

The `NexworkApp` module contains the core functionality of the system:

- `views.py`: Contains the logic for each section (profile, posts, stories, jobs, requests, etc.).
- `models.py`: Defines all database models (users, jobs, applications, messages, etc.).
- `forms.py`: Custom forms used for registration, posting, job applications, and more.
- `templatetags/`: Custom Django template filters (e.g., date formatting, name extraction).
- `migrations/`: Contains Django-generated migrations to create and modify the database.

---

### 🎨 Templates

HTML views are organized as follows:

- `templates/Nexwork/layouts/`: Base UI structure (navigation bar, general layout).
- `templates/Nexwork/auth/`: Authentication views like login and registration.
- Other views are organized by specific modules (profile, posts, stories, statistics, etc.).

---

### 🖼️ Static Files

Static assets are located in:

- `static/css/`, `static/js/`, `static/images/`: Contains project stylesheets, custom scripts, and images.
- `static/bootstrap-5.3.3/`: Local version of Bootstrap used in the UI.
- `static/js/Nexwork/auth/`: Scripts specifically for login, registration, and validations.
- `static/media/`: Reserved folder for media files (profile images, banners, etc.).

---

### ⚙️ Project Base: NexworkProject

This directory contains the main Django configuration files:

- `settings.py`: Main project configuration.
- `urls.py`: URL and view routing.
- `asgi.py / wsgi.py`: Entry points for ASGI/WSGI servers.

---

## 📄 About & License

This project was originally developed in 2025 as the final project for the [**CS50’s Web Programming with Python and JavaScript**](https://cs50.harvard.edu/web/2020/projects/final/capstone/) course from HarvardX.

The current main version is on the `main` branch and has been enhanced with new features since its initial submission: real-time messaging, visual statistics, job application system, stories, and a fully responsive design.

This is a personal, open-source project distributed under the **MIT License**. You are free to use, study, modify, or distribute it under the terms of that license.

**Nexwork** is provided “as is”, without any warranty. The author is not responsible for any damage, data loss, or inconvenience caused by using this software.

If you enjoyed this project, consider supporting the developer by leaving a ⭐ on [GitHub](https://github.com/JJuan777/Nexwork)!

<details>
<summary><strong>📦 Railway Deployment</strong></summary>

## 📦 Railway Deployment <a name="deploy-railway"></a>

The project was deployed to production using **[Railway](https://railway.app)**, a platform that automates the building and deployment of applications with support for Docker and environment variables.

### 🔧 Configuration Used

- **Dockerfile**:

```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8001
CMD ["gunicorn", "NexworkProject.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "3"]
```

- **runtime.txt**:

```txt
3.12
```

- **settings.py (production)**:

```python
ALLOWED_HOSTS = ['localhost', 'nexwork-app.up.railway.app']
PORT = os.getenv('PORT', '8001')
CSRF_TRUSTED_ORIGINS = ['https://web-production-bb26.up.railway.app']
```

### 🔄 For Other Environments

To deploy on other platforms:

- Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` as needed.
- Adjust the port number if required.
- Alternatively, you can use a `Procfile`:

```txt
web: gunicorn NexworkProject.wsgi:application --bind 0.0.0.0:$PORT --workers 3
```

🔗 Project repository: [https://github.com/JJuan777/Nexwork](https://github.com/JJuan777/Nexwork)

</details>
