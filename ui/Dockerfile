FROM node:lts-slim

RUN npm install -g pnpm

WORKDIR /app/ui

COPY ./ui/package.json ./ui/pnpm-lock.yaml* ./ui/pnpm-workspace.yaml ./
RUN pnpm install && \
    rm -f package.json pnpm-lock.yaml pnpm-workspace.yaml && \
    chown node:node -R node_modules

COPY --chown=node:node ./ui .

RUN npm run build && \
    chown node:node -R .next

EXPOSE 3000
