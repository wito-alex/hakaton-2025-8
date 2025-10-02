# Use an official Node.js runtime as a parent image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /home/frontend

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json /home/frontend/

# Install project dependencies
RUN npm install

# Copy the rest of the application's code
COPY . .

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define the command to run the app
CMD ["npm", "run", "dev"]