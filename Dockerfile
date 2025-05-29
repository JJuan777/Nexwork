# Usa una imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt y instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación al contenedor
COPY . .

# Recolecta archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto en el que el contenedor escuchará
EXPOSE 8081

# Comando para iniciar la aplicación usando Gunicorn
CMD ["gunicorn", "NexworkProject.wsgi:application", "--bind", "0.0.0.0:8081", "--workers", "3"]
