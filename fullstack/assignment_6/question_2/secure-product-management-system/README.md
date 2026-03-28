# Secure Product Management System (RBAC + JWT)

A React application with mocked JWT authentication and role-based access control using JSON Server.

## Features
- Register and login with mocked JWT token
- Context API auth state for token, role, and user
- Protected routes and role-protected routes
- Product CRUD restricted to admin
- Product view for both admin and user
- Jest test coverage for auth, RBAC, products, and dashboard

## Run

1. Install dependencies

```bash
npm install
```

2. Start backend (JSON Server)

```bash
npx json-server --watch backend/db.json --port 3000
```

3. Start frontend

```bash
npm start
```

Frontend runs at http://localhost:3001 and backend at http://localhost:3000.

## Tests

```bash
npm test
```

Specific test:

```bash
npm test RBAC.test.js
```

Watch mode:

```bash
npm test -- --watch
```
