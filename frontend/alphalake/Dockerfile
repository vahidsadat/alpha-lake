FROM node:20-alpine

WORKDIR /app

COPY frontend/alphalake/package*.json ./
RUN npm install

# Copy the rest of the source code
COPY frontend/alphalake/. .

# Set Environment variables
ENV NEXT_TELEMETRY_DISABLED=1

# Metadata for documentation
EXPOSE 3000

RUN npm run build

CMD [ "npm", "start" ]