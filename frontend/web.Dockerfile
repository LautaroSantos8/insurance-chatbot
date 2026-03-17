# Stage 1: Build 
FROM node:20.14.0 as build 

WORKDIR /app 
COPY package*.json ./ 
RUN npm install 
COPY . . 

# Use the build argument to set the environment variable
ARG VITE_API_KEY
ENV VITE_API_KEY=${VITE_API_KEY}

# Build the application 
RUN npm run build 

# Stage 2: Serve 
FROM nginx:alpine 
COPY --from=build /app/dist /usr/share/nginx/html 

# Copy custom Nginx configuration if needed 
#COPY nginx.conf /etc/nginx/nginx.conf 

EXPOSE 80 
CMD ["nginx", "-g", "daemon off;"]
