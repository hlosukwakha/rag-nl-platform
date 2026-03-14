FROM node:20-alpine
WORKDIR /app
COPY apps/nextjs-ui/package.json /app/package.json
RUN npm install
COPY apps/nextjs-ui /app
RUN npm run build
CMD ["npm", "run", "start"]
