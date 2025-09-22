# CBDE_Lab1

Proyecto Hecho por Adrián Ferrer Gutierrez y Francesc Pérez Venegas

# Proyecto de Comparación de Bases de Datos Vectoriales

Este proyecto tiene como objetivo comparar el rendimiento de diferentes enfoques para almacenar y consultar embeddings de frases, con el fin de encontrar las más similares entre sí. Se evalúan tres implementaciones principales:

1.  **PostgreSQL con la extensión `pgvector`**: Aprovecha las capacidades nativas de la base de datos para realizar búsquedas de similitud de manera eficiente.
2.  **PostgreSQL sin extensiones vectoriales**: Almacena los embeddings como arrays y realiza los cálculos de similitud en el lado del cliente (Python con NumPy).
3.  **ChromaDB**: Utiliza una base de datos vectorial nativa que gestiona automáticamente la creación y consulta de embeddings.

## Prerrequisitos

Antes de empezar, asegúrate de tener instalado lo siguiente:

- Python 3.8 o superior.
- PostgreSQL (versión 12 o superior recomendada).
- La extensión `pgvector` para PostgreSQL. Puedes encontrar las instrucciones de instalación en su [repositorio oficial](https://github.com/pgvector/pgvector).
- Un servidor de PostgreSQL en ejecución.

**Nota**: Los scripts de PostgreSQL están configurados para conectarse con las siguientes credenciales:
- **Base de datos**: `postgres`
- **Usuario**: `postgres`
- **Contraseña**: `1234`
- **Host**: `localhost`

Si tu configuración es diferente, por favor, modifica las credenciales en los scripts correspondientes (`.py`).

## Configuración del Proyecto

1.  **Clonar el repositorio**:
    ```bash
    git clone <URL-del-repositorio>
    cd <nombre-del-directorio>
    ```

2.  **Crear un entorno virtual**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    ```

3.  **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Descargar el dataset**:
    Asegúrate de que el archivo `bookcorpus_10k_sentences.csv` se encuentre en el directorio raíz del proyecto.

## Cómo Ejecutar los Scripts

A continuación se detalla el orden de ejecución para cada una de las implementaciones.

### Implementación G: PostgreSQL con `pgvector`

Este enfoque utiliza `pgvector` para realizar los cálculos de similitud directamente en la base de datos.

1.  **Cargar las frases en la base de datos**:
    ```bash
    python G0_load_sentences.py
    ```

2.  **Generar y almacenar los embeddings**:
    ```bash
    python G1_generate_store_embeddings.py
    ```

3.  **Realizar consultas de similitud**:
    ```bash
    python G2_query_similarities.py
    ```

### Implementación P: PostgreSQL sin `pgvector`

Este enfoque carga todos los embeddings en memoria y realiza los cálculos con Python.

1.  **Cargar las frases en la base de datos**:
    ```bash
    python P0_load_senteces.py
    ```

2.  **Generar y almacenar los embeddings** (elige una de las dos alternativas):
    - **Alternativa 1: Una sola tabla** (embeddings en la misma tabla que las frases):
      ```bash
      python P1_alternative_1_table.py
      ```
    - **Alternativa 2: Dos tablas** (embeddings en una tabla separada):
      ```bash
      python P1_generate_store_embeddings_2tables.py
      ```

3.  **Realizar consultas de similitud**:
    - Si usaste la **Alternativa 1** (una tabla):
      ```bash
      python P2_query_similarities.py
      ```
    - Si usaste la **Alternativa 2** (dos tablas):
      ```bash
      python P2_query_similarities_done.py
      ```

### Implementación C: ChromaDB

Este enfoque utiliza una base de datos vectorial nativa que abstrae la generación y almacenamiento de embeddings.

1.  **Cargar frases y generar embeddings** (ChromaDB lo hace en un solo paso):
    ```bash
    python "C0_load_sentences_&_C1_embeddings.py"
    ```

2.  **Realizar consultas de similitud**:
    ```bash
    python C2_query_similarities.py
    ```
