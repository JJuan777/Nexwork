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

# Expone el puerto de escucha (opcional)
EXPOSE 8080

# Comando para iniciar la aplicación con Gunicorn usando el puerto de Railway
CMD ["gunicorn", "NexworkProject.wsgi:application", "--bind", "0.0.0.0:${PORT}", "--workers", "3"]
