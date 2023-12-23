# Используем официальный образ Node.js
FROM node:latest

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app/public

# Копируем файлы package.json и package-lock.json
COPY package*.json ./


RUN npm config set registry https://registry.npmjs.org/

# Устанавливаем зависимости
RUN npm install

# Копируем все файлы из текущей директории внутрь контейнера
COPY . .

# Собираем React-приложение
RUN npm run build

# Открываем порт для доступа к приложению (если приложение использует другой порт, его нужно указать)
EXPOSE 3000

# Запускаем приложение при старте контейнера
CMD ["npm", "start"]