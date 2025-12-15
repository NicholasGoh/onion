FROM node:lts-slim

RUN npm install -g pnpm

WORKDIR /app

COPY ./ui/package.json ./ui/pnpm-lock.yaml* ./
RUN pnpm install && \
    rm -f package.json pnpm-lock.yaml && \
    chown node:node -R node_modules

COPY --chown=node:node ./ui .

RUN npm run build && \
    chown node:node -R .next

EXPOSE 3000
