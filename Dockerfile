# ── Stage 1: Build React frontend ────────────────────────────────────────────
FROM node:20-slim AS frontend-build

WORKDIR /app/web/frontend
COPY web/frontend/package.json ./
RUN npm install
COPY web/frontend/ ./
RUN npm run build

# ── Stage 2: Final runtime image ──────────────────────────────────────────────
FROM node:20-slim

# Install Python 3 + pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip3 install --break-system-packages -r requirements.txt

# Install Node backend dependencies (production only)
COPY web/backend/package.json ./web/backend/
RUN cd web/backend && npm install --omit=dev

# Copy Python simulator
COPY qkd_simulator.py ./

# Copy Node backend
COPY web/backend/ ./web/backend/

# Copy compiled React app from stage 1
COPY --from=frontend-build /app/web/frontend/build ./web/frontend/build

ENV PYTHON_BIN=python3
# PORT is set by Render/Railway automatically
EXPOSE 3001

CMD ["node", "web/backend/server.js"]
