# Virtual Environment Set-Up
Instead of Pip, we choose to work with `uv`. It is the modern light weight and powerful dependency manager, it fast and very reliable cos its written in **Rust**.

### The Standard Workflow

1. Initialize: `uv init`
    - Creates your project structure and pyproject.toml.

2. Add Tools: `uv add pandas sqlalchemy psycopg2-binary`
    - This updates the "Shopping List" and "Receipt" automatically.

3. Sync (The "Fixer"): `uv sync`
    - Ensures your .venv perfectly matches your uv.lock. If you delete your .venv, this command brings it back to life.

4. Execute: `uv run python script.py`
    - The "Silver Bullet." It handles the environment context so you don't have to manually "activate" anything.

### Component and Role
- `pyproject.toml`: The Manifest >> Our Shopping List: It says "I need Pandas and SQLAlchemy."
- `uv.lock`: The State >> Our Receipt. It records the exact version and "fingerprint" of every library.
- `.venv/`:	The Workspace >> The Kitchen. Where the actual work happens. It's replaceable!


### Benefits of `uv`:
1. Isolation is Guaranteed: Project A's libraries never touch Project B's.

2. Version Pinning: The uv.lock file means you never accidentally upgrade a library that breaks your database connection.

3. Portability: When you eventually move your code into a Docker Image, you simply tell Docker: "Look at my uv.lock and build this exact same environment."



# Docker Fundamentals

Docker is a _containerization software_ that allows us to isolate software in a similar way to virtual machines but in a much leaner way.

- Docker is like a portable house for storing and keeping essitials only associated within it.
To run docker, we use the command `docker run <DOCKER FILE NAME>`. To be able to interact with the docker file we run in `-it`as in `docker run -it <DOCKER FILE NAME>`, e.g. 
```bash 
docker run -it ubuntu
```

A Docker image is a _snapshot_ of a container that we can define to run our software, or in this case our data pipelines. By exporting our Docker images to Cloud providers such as Amazon Web Services or Google Cloud Platform we can run our containers there.

## Why Docker?

Docker provides the following advantages:

- Reproducibility: Same environment everywhere
- Isolation: Applications run independently
- Portability: Run anywhere Docker is installed

They are used in many situations:

- Integration tests: CI/CD pipelines
- Running pipelines on the cloud: AWS Batch, Kubernetes jobs
- Spark: Analytics engine for large-scale data processing
- Serverless: AWS Lambda, Google Functions

## Basic Docker Commands

Check Docker version:

```bash
docker --version
```


- Docker is stateless, which means after running a file any new activity created within it is not actively saved when you return into the container. Run `docker ps -aq` to see the list of created docker volumes (id) and `docker ps -a` to see the list of docker images. To remove all existing volumes (images), run `docker rm 'docker ps -aq'`

## Docker Compose

In the early days, we had to manually configure IP addresses and network bridges just to get a database to talk to a UI. Today, we use **Docker Compose**

Imagine a docker-compose.yaml file as a blueprint for a mini-datacenter that lives on your laptop. Instead of one giant computer, we’re building a cluster of specialized "rooms" (containers) that are wired together perfectly.

- ### Anatomy of a docker image file (.yaml)
```bash 
services:
  pgdatabase:
    image: postgres:18
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "root"
      POSTGRES_DB: "ny_taxi"
    volumes:
      - ny_taxi_postgres_data:/var/lib/postgresql
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: "admin@admin.com"
      PGADMIN_DEFAULT_PASSWORD: "root"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    ports:
      - "8085:80"

volumes:
  ny_taxi_postgres_data:
  pgadmin_data:
```
### 1. Services: The "Rooms"

This section defines the containers we want to run. In this module, we usually have two:

- `pgdatabase`: This is your "Engine Room." It’s running Postgres 18.

- `pgadmin`: This is your "Control Tower." It’s a web-based GUI to manage the engine room

### 2. Ports: The "Gateways"

This is where traffic flows from your laptop into the containers.

    Postgres (5432:5432): Standard. You talk to Postgres on your machine using the default port.

    pgAdmin (8085:80): Notice the change here. Internally, pgAdmin listens on port 80 (HTTP). You’ve mapped it so that you access it in your browser via localhost:8085.

### 3. Environment: The "Keys"

This is where we set our passwords and usernames:

    POSTGRES_USER=root

    POSTGRES_PASSWORD=root

    POSTGRES_DB=ny_taxi 
**Tip:** In a real production environment, we’d use secrets, but for learning, hard-coding these is fine—just don't do it with your bank password!

### 4. Ports: The "Windows"

`ports: - "5432:5432"`

The left side is your laptop (the Host).

The right side is the inside of the container. This maps your laptop’s port 5432 to the database’s port 5432. It’s like a wormhole between your computer and the container.

### 5. Volumes: The "Pantry"
```bash
volumes:
      - ny_taxi_postgres_data:/var/lib/postgresql
```

This is the most "Senior" part of your YAML.

Containers are ephemeral—meaning if you stop them, they "forget" everything. Volumes are folders on your Linux system that stay put. By "mounting" this volume, your data survives even if you delete the container.

## Connecting a volume to a local directory
Lets say we have a `python` container. If we want bash, we need to overwrite `entrypoint` with `bash`:

```bash
docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.9.16-slim
```
Now we can map a local repository to the `python` container 
```bash
docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \
    --entrypoint=bash \
    python:3.9.16-slim
```
Inside the python container, we can run python scrips that acces docs from the local repository.


# Docker images: A Data Pipeline example
Now, let's "containerize" a pipeline. We need a Dockerfile that takes the python code and the uv environment, then bakes them into an image.

A **data pipeline** is a service that receives data as input and outputs more data. For example, reading a CSV file, transforming the data somehow and storing it as a table in a PostgreSQL database.

In short, A data pipeline is a process that takes data from one point to another

```mermaid
graph LR
    A[CSV File] --> B[Data Pipeline]
    B --> C[Parquet File]
    B --> D[PostgreSQL Database]
    B --> E[Data Warehouse]
    style B fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
```
To create a data pipeline for the `pipeline.py` script, we Create a simple `Dockerfile` file for it as follows:
```bash
FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# Now we copy from the perspective of the project root
COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked

# Copy the pipeline script specifically from the module folder
COPY M01-docker-terraform/pipeline.py .

ENTRYPOINT ["python", "pipeline.py" ]
```


Let's break down your specific recipe line-by-line.
1. The Foundation (FROM)

```bash
FROM ghcr.io/astral-sh/uv:python3.12-alpine
```
Concept: Every image starts with a parent.
python3.12: The Python version.
alpine: A tiny, 5MB version of Linux. Industry pros love it because it’s secure and lightweight.
uv: This base already has the uv tool pre-installed.

2. The Context (WORKDIR)

`WORKDIR /app`

Concept: This is the internal cd command.Everything we do from here on happens inside a folder named /app inside the image. It keeps our "frozen computer" tidy.

3. The Wiring (ENV PATH)
```bash
ENV PATH="/app/.venv/bin:$PATH"
```
Concept: Setting the "Look Here First" rule.When uv installs packages, it puts them in a virtual environment (.venv). This line tells the computer: "When I type python, look inside the .venv folder before looking anywhere else."

4. The Manifests (COPY)
```bash
COPY pyproject.toml .python-version uv.lock ./
```
Concept: Moving the "Shopping List" from your laptop into the image. We copy these files first and separately. Why? Layer Caching. Docker remembers that it has already seen these files. If you change your code but not your libraries, Docker will skip the expensive "install" step next time you build.

5. The Build Step (RUN)

`RUN uv sync --locked`

Concept: Actually doing the work. This command runs during the build phase. It downloads all the libraries in your uv.lock and creates the environment. Once this is done, those libraries are "baked" into the image forever.

6. The Logic (COPY)
```bash
COPY M01-docker-terraform/pipeline.py .
```
Concept: Moving the actual "Brain" of the operation. We copy your script last. Since your code changes more often than your libraries, putting this last ensures your builds stay lightning-fast.

7. The Default Command (ENTRYPOINT)
`ENTRYPOINT ["python", "pipeline.py" ]`

Concept: The "Play" button. This tells the container what to do the moment it wakes up. When you run the container, it immediately executes python pipeline.py.


---

# Building Docker Images: Project-Wide Guide

This section explains how to correctly build Docker images in this project structure and avoid common pitfalls when working with multiple module directories (M01, M02, M03, etc.).

## The Problem We Solved

When building the `taxi_ingest:v001` image, we encountered two issues:

| Issue | Cause | Solution |
|-------|-------|----------|
| `COPY failed: file not found` | Running `docker build .` from inside `M01-docker-terraform/` but Dockerfile referenced `pyproject.toml` in parent directory | Build from project root using `-f` flag |
| `can't stat 'ny_taxi_postgres_data'` | Docker tried to include PostgreSQL data files with permission restrictions | Added `.dockerignore` in project root |

## Why Always Build from Project Root?

### Project Structure Reality

```
de-zoomcamp/                    ← PROJECT ROOT (build context)
├── pyproject.toml              ← Shared dependency manifest
├── .python-version             ← Shared Python version
├── uv.lock                     ← Shared lockfile
├── .dockerignore               ← Excludes problematic files
├── M01-docker-terraform/
│   ├── Dockerfile
│   └── injest_data.py
├── M02-workflow-orchestration/
│   ├── Dockerfile              ← Future Dockerfiles
│   └── some_script.py
├── M03-data-warehouse/
│   ├── Dockerfile
│   └── another_script.py
└── ny_taxi_postgres_data/      ← Excluded by .dockerignore
```

### The Core Constraint

Docker's `COPY` command **cannot access files outside the build context**. Since all modules share:
- `pyproject.toml` (dependencies)
- `.python-version` (Python version)
- `uv.lock` (locked versions)

These files live in the **project root**, so the build context **must** be the project root.

### The Correct Build Pattern

```bash
# Always run from project root
cd /home/ridwan/Desktop/PROJECTS/Data_Engineering/de-zoomcamp

# Use -f to specify which Dockerfile to use
docker build -t <image_name>:<tag> -f <module>/Dockerfile .
```

**Examples for each module:**

```bash
# M01
docker build -t taxi_ingest:v001 -f M01-docker-terraform/Dockerfile .

# M02 (future)
docker build -t workflow_tool:v001 -f M02-workflow-orchestration/Dockerfile .

# M03 (future)
docker build -t warehouse_loader:v001 -f M03-data-warehouse/Dockerfile .
```

### What `-f` Does

| Flag | Purpose |
|------|---------|
| `-f M01-docker-terraform/Dockerfile` | Tells Docker which Dockerfile to read |
| `.` (at the end) | Sets the build context to current directory (project root) |

## Writing Dockerfiles for Any Module

When creating a new Dockerfile in M02, M03, or any other module, follow this template:

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# Step 1: Copy shared dependency files from project root
COPY pyproject.toml .python-version uv.lock ./

# Step 2: Install dependencies
RUN uv sync --locked

# Step 3: Copy YOUR module's script (use full path from project root)
COPY M02-workflow-orchestration/your_script.py .
#     ^^^^^^^^^^^^^^^^^^^^^^^^^ 
#     Full path from project root, NOT relative to Dockerfile location

ENTRYPOINT ["python", "your_script.py"]
```

### Key Rule for COPY Paths

| Scenario | Wrong ❌ | Correct ✅ |
|----------|---------|-----------|
| Copying script from M02 | `COPY your_script.py .` | `COPY M02-workflow-orchestration/your_script.py .` |
| Copying folder from M03 | `COPY src/ .` | `COPY M03-data-warehouse/src/ .` |

The path is **always relative to the build context (project root)**, not relative to where the Dockerfile is located.

## Understanding .dockerignore

### Why We Need It

The `.dockerignore` file sits in the **project root** and tells Docker which files/folders to exclude from the build context.

**Location:** `/home/ridwan/Desktop/PROJECTS/Data_Engineering/de-zoomcamp/.dockerignore`

**Current contents:**
```
ny_taxi_postgres_data/
.git/
__pycache__/
*.pyc
.venv/
```

### What Each Line Does

| Pattern | Purpose |
|---------|---------|
| `ny_taxi_postgres_data/` | Excludes PostgreSQL data files (permission issues, large size) |
| `.git/` | Excludes Git history (unnecessary in container, large) |
| `__pycache__/` | Excludes Python bytecode cache |
| `*.pyc` | Excludes compiled Python files |
| `.venv/` | Excludes local virtual environment (container builds its own) |

### Why This Matters for Future Modules

When you add new modules (M02, M03, etc.), the **same `.dockerignore`** applies to all builds because:
1. You always build from project root
2. `.dockerignore` must be in the build context root
3. One file covers all modules

### When to Update .dockerignore

Add new entries when:
- A module generates large data files (e.g., `M02-workflow-orchestration/output_data/`)
- You have credentials or secrets that shouldn't be in images
- Build fails due to permission errors on specific directories

**Example addition for M02:**
```
ny_taxi_postgres_data/
.git/
__pycache__/
*.pyc
.venv/
M02-workflow-orchestration/large_dataset/
```

## Quick Reference Checklist

Before building any Docker image in this project:

- [ ] Am I in the **project root** directory? (`de-zoomcamp/`)
- [ ] Does my Dockerfile use **full paths from project root** for COPY commands?
- [ ] Is `.dockerignore` present in project root?
- [ ] Am I using `-f <module>/Dockerfile .` in my build command?

## Common Errors and Fixes

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `COPY failed: file not found in build context` | Wrong COPY path or wrong build directory | Build from project root, use full path in COPY |
| `forbidden path outside the build context` | Using `../` in COPY path | Never use `..`, build from project root instead |
| `can't stat '<directory>'` | Permission issues on a directory | Add directory to `.dockerignore` |
| `Sending build context to Docker daemon  X GB` | Too many files being sent | Add large directories to `.dockerignore` |

---

# Running PostgresSQL in a Container



