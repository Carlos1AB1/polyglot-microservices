# Arquitectura de Microservicios Políglota

![Arquitectura de Microservicios](https://img.shields.io/badge/Arquitectura-Microservicios-blue)
![Java](https://img.shields.io/badge/Java-17-orange)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.0-brightgreen)
![Spring Cloud](https://img.shields.io/badge/Spring%20Cloud-2023.0.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![MySQL](https://img.shields.io/badge/Base%20de%20Datos-MySQL-blue)

Una demostración de arquitectura de microservicios políglota que muestra la integración de servicios Java y Python trabajando juntos a través de un API Gateway común y un patrón de Descubrimiento de Servicios.

## Arquitectura del Sistema

Este proyecto implementa una arquitectura escalable de microservicios políglota con los siguientes componentes:

- **Descubrimiento de Servicios** (Java - Eureka Server): Registro central para todos los microservicios
- **API Gateway** (Java - Spring Cloud Gateway): Punto de entrada único para las solicitudes de los clientes
- **Servicio de Productos** (Java - Spring Boot): Gestiona los datos de productos
- **Servicio de Pedidos** (Python - Django): Gestiona el procesamiento de pedidos

![Diagrama de Arquitectura](https://www.mermaidchart.com/raw/68aad81a-4b88-42a8-925b-dbbae35e0d70?theme=light&version=v0.1&format=svg)



## Componentes

### Servicios Java

#### Servidor Eureka

Servidor de descubrimiento de servicios que permite a los microservicios registrarse y descubrir otros servicios registrados.

- Puerto: 8761
- URL: http://localhost:8761

#### API Gateway

Enruta las solicitudes de los clientes a los servicios apropiados.

- Puerto: 8080
- Rutas:
  - `/api/products/**` → Servicio de Productos (Java)
  - `/api/orders/**` → Servicio de Pedidos (Python)

#### Servicio de Productos

Gestiona los datos de productos a través de una API RESTful.

- Puerto: 8081
- Endpoints:
  - `GET /products`: Obtener todos los productos
  - `GET /products/{id}`: Obtener producto por ID
  - `POST /products`: Crear un nuevo producto
  - `PUT /products/{id}`: Actualizar un producto existente
  - `DELETE /products/{id}`: Eliminar un producto

### Servicios Python

#### Servicio de Pedidos

Gestiona los datos de pedidos a través de una API RESTful.

- Puerto: 8083
- Endpoints:
  - `GET /orders`: Obtener todos los pedidos
  - `GET /orders/{id}`: Obtener pedido por ID
  - `POST /orders`: Crear un nuevo pedido
  - `PUT/PATCH /orders/{id}`: Actualizar un pedido existente
  - `DELETE /orders/{id}`: Eliminar un pedido

## Requisitos Previos

- JDK 17 o posterior
- Python 3.10 o posterior
- MySQL 8.0+
- Maven 3.8+
- pip

## Configuración de la Base de Datos

Configura dos bases de datos MySQL:

1. **Base de Datos del Servicio de Productos**
   ```sql
   CREATE DATABASE db_product_service;
   CREATE USER 'polyglot_user'@'localhost' IDENTIFIED BY 'polyglot_pass';
   GRANT ALL PRIVILEGES ON db_product_service.* TO 'polyglot_user'@'localhost';
   ```

2. **Base de Datos del Servicio de Pedidos**
   ```sql
   CREATE DATABASE db_order_service;
   GRANT ALL PRIVILEGES ON db_order_service.* TO 'polyglot_user'@'localhost';
   ```

## Instalación y Configuración

### Servicios Java

1. Clona el repositorio
   ```bash
   git clone <url-del-repositorio>
   cd java-services
   ```

2. Construye el proyecto
   ```bash
   mvn clean package
   ```

3. Inicia los servicios en el siguiente orden:
   ```bash
   # Inicia el Servidor Eureka
   java -jar eureka-server/target/eureka-server-0.0.1-SNAPSHOT.jar
   
   # Inicia el Servicio de Productos
   java -jar product-service/target/product-service-0.0.1-SNAPSHOT.jar
   
   # Inicia el API Gateway
   java -jar gateway-service/target/gateway-service-0.0.1-SNAPSHOT.jar
   ```

### Servicio de Pedidos Python

1. Navega al directorio del Servicio de Pedidos
   ```bash
   cd order-service
   ```

2. Crea y activa un entorno virtual
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias
   ```bash
   pip install -r requirements.txt
   ```

4. Aplica las migraciones de la base de datos
   ```bash
   python manage.py migrate
   ```

5. Inicia el servicio
   ```bash
   python manage.py runserver 8083
   ```

## Prueba de los Servicios

Una vez que todos los servicios estén funcionando, puedes acceder a:

- **Panel de Eureka**: http://localhost:8761
- **API de Productos**: http://localhost:8080/api/products
- **API de Pedidos**: http://localhost:8080/api/orders

## Ejemplo de Uso de la API

### Crear un Producto

```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Smartphone","price":799.99}'
```

### Crear un Pedido

```bash
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Juan Pérez","product_id":1,"quantity":2}'
```

## Estructura del Proyecto

```
├── java-services/
│   ├── eureka-server/        # Descubrimiento de Servicios
│   ├── gateway-service/      # API Gateway
│   └── product-service/      # Microservicio de Productos (Java)
│
└── order-service/            # Microservicio de Pedidos (Python/Django)
```

## Ampliación del Sistema

Para añadir un nuevo microservicio:

1. Crea tu servicio (Java o cualquier lenguaje)
2. Regístralo con Eureka (ver ejemplos en el código Java o Python)
3. Añade una ruta en la configuración del API Gateway

## Licencia

[Licencia MIT](LICENSE)

## Colaboradores

- Tu Nombre - Trabajo inicial
