# 1. Fase de construcción
FROM node:18-alpine AS build

# 2. Establece el directorio de trabajo
WORKDIR /app

# 3. Copia los archivos de configuración y las dependencias
COPY ./frontend/package*.json ./



# 4. Instala las dependencias
RUN npm install

# 5. Copia el resto del código fuente
COPY ./frontend .



# 7. Si necesitas que sea una variable de entorno, define ENV
#ENV VITE_API_URL="/api"

# 6. Construye la aplicación
RUN npm run build



# Imagen base
FROM nginx:alpine

# Instalación de dependencias
RUN apk add --no-cache python3 py3-pip \
    supervisor 
    #&& pip install --upgrade pip \
    #&& pip install virtualenv

# Crear carpetas necesarias
RUN mkdir -p /app/frontend/build /app/backend
RUN mkdir -p /app/logs

# Copiar el código de la API y frontend
COPY backend /app/backend
#  Copia los archivos construidos desde la fase anterior
COPY --from=build /app/dist /app/frontend/build

COPY web/nginx.conf /etc/nginx/nginx.conf
COPY web/default.conf /etc/nginx/conf.d/default.conf

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf



# Instalar dependencias de la API en un entorno virtual


WORKDIR /app/backend
RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip install -r requirements.txt

# Exponer puertos
EXPOSE 81 80 82



# Comando de inicio
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
