# Smart Inventory Management System

A React application with authentication and product inventory CRUD using JSON Server.

## Features
- Register and login
- Global authentication state via Context API
- Protected dashboard route
- Product create, read, update, delete
- Jest and React Testing Library test coverage

## Project Structure

```text
smart-inventory-management-system/
  backend/
    db.json
  src/
    components/
    context/
    pages/
    routes/
    services/
    tests/
```

## Setup

1. Install dependencies:

```bash
npm install
```

2. Start JSON Server:

```bash
npx json-server --watch backend/db.json --port 3000
```

3. Start React app:

```bash
npm start
```

The frontend starts on http://localhost:3001 and communicates with JSON Server on port 3000.

## Run Tests

```bash
npm test
```

Specific test file:

```bash
npm test Login.test.js
```

Watch mode:

```bash
npm test -- --watch
```
