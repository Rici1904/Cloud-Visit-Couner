☁️ Cloud-Visit-Counter – Modul 210 Projekt

Dieses Projekt implementiert eine hochverfügbare Microservice-Architektur in Kubernetes. Die Anwendung ist ein einfacher Besucherzähler, bei dem der Fokus auf der automatisierten Konfiguration, Persistenz (PVC) und der Fehlerresistenz (Readiness Probes) der Infrastruktur liegt.

🛠️ Technologien im Einsatz

Applikation: Python 3.9 (Flask)

Datenhaltung: Redis (Offizielles Docker Image)

Containerisierung: Docker

Orchestrierung: Kubernetes (YAML Manifeste)

CI/CD: GitLab CI / GitHub Actions (Konfiguration in .gitlab-ci.yaml)

🧱 Architektur (Zwei Komponenten)

Das System besteht aus zwei Services, die über Kubernetes miteinander kommunizieren:

counter-api-deployment: Der Stateless Web-Service (Python/Flask), der Anfragen verarbeitet und den Zähler in Redis inkrementiert.

Verfügt über Readiness und Liveness Probes (/health Endpunkt), um den stabilen Start zu gewährleisten.

redis-cache-deployment: Der Stateful Caching-Layer.

Daten werden über einen Persistent Volume Claim (PVC) gesichert.

🚀 Inbetriebnahme (Hands-off Installation)

Das System ist für die "Hands-off Installation" konzipiert. Es wird davon ausgegangen, dass ein Kubernetes Cluster (z.B. Docker Desktop Kubernetes) und kubectl konfiguriert sind.

1. Dateien und Image-Vorbereitung

Stellen Sie sicher, dass das API-Image (cloud-visit-counter-api:v1.3) gebaut und im Cluster sichtbar ist.

Manuelle Speichervorbereitung: Die manuelle Erstellung des Persistent Volume (PV) ist in der lokalen Testumgebung einmalig notwendig:

kubectl apply -f pv-redis-manual.yaml


2. Deployment

Wenden Sie alle Konfigurationsdateien im Wurzelverzeichnis an, um das gesamte System (API, Redis, PVC, Services) zu starten:

kubectl apply -f .


3. Funktionstest

Warten Sie, bis alle Pods den Status 1/1 Running erreicht haben.

Port ermitteln:

kubectl get services counter-api-service


Merken Sie sich den zugewiesenen NodePort (z.B. 32388)

Test im Browser:
Öffnen Sie die Anwendung unter der Host-Adresse und dem ermittelten Port:

http://localhost:[NodePort]
# Beispiel: http://localhost:32388


📄 Wichtige Konfigurationsdateien

Datei

Zweck

api-deployment.yaml

Definiert das API Deployment, den LoadBalancer Service und die Readiness/Liveness Probes.

redis-deployment.yaml

Definiert das Redis Deployment, den internen ClusterIP Service und bindet das PVC.

pvc-redis.yaml

Fordert den persistenten Speicherplatz (1Gi) für Redis an.

app.py

Python-Anwendungscode mit fehlerresistenter Redis-Verbindungslogik und /health Endpunkt.

.gitlab-ci.yaml

Definiert die Pipeline-Phasen (Build, Push, Deploy).