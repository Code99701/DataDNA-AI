# Goal Description

The goal is to implement a secure login system to ensure that only authorized users can view the dashboard and the underlying data. We will achieve this by adding JSON Web Token (JWT) based authentication to the FastAPI backend and modifying the frontend to handle login, token storage, and authenticated API requests.

## User Review Required

> [!IMPORTANT]  
> We need to introduce new dependencies (`python-jose` and `passlib[bcrypt]`), which will require a pip install on the backend.
> Also, currently there is no user registration flow in the UI. Should we build a registration page as well, or initially include a default admin user/allow open registration through an API only? My current plan includes open registration via the login page (or a toggle on the login page).

## Proposed Changes

### Backend

#### [MODIFY] [requirements.txt](file:///d:/google%20solutions/Google-Solutions-2026-Project/backend/requirements.txt)
- Add `python-jose[cryptography]`, `passlib[bcrypt]`, and `bcrypt` for JWT generation and password hashing.

#### [MODIFY] [config.py](file:///d:/google%20solutions/Google-Solutions-2026-Project/backend/app/core/config.py)
- Add environment variables/constants for `SECRET_KEY`, `ALGORITHM` (HS256), and `ACCESS_TOKEN_EXPIRE_MINUTES`.

#### [NEW] [auth.py](file:///d:/google%20solutions/Google-Solutions-2026-Project/backend/app/api/routes/auth.py)
- Add an API router with two endpoints:
  - `POST /auth/register` to create a new user in MongoDB.
  - `POST /auth/token` to verify credentials and return a Bearer JWT.

#### [MODIFY] [dependencies.py](file:///d:/google%20solutions/Google-Solutions-2026-Project/backend/app/api/dependencies.py)
- Fully implement `get_current_user` using `OAuth2PasswordBearer` to decode and validate the token from the request header.

#### [MODIFY] [files.py](file:///d:/google%20solutions/Google-Solutions-2026-Project/backend/app/api/routes/files.py)
- Inject `Depends(get_current_user)` into `GET /files/` and `GET /files/stats` to require an authorized token.

#### [MODIFY] [main.py](file:///d:/google%20solutions/Google-Solutions-2026-Project/backend/app/main.py)
- Inject the `auth.router` into the main FastAPI application.

---

### Frontend

#### [NEW] [login_frontend.html](file:///d:/google%20solutions/Google-Solutions-2026-Project/frontend/login_frontend.html)
- A beautifully designed login page consistent with the project's established styling (Tailwind CSS, Material Symbols).
- Forms to support both login and a toggle for user registration.
- JavaScript to call the backend `/auth/token` (and `/auth/register`) and store the resulting JWT in `localStorage`.
- On success, redirect to `dashboard_frontend.html`.

#### [MODIFY] [dashboard_frontend.html](file:///d:/google%20solutions/Google-Solutions-2026-Project/frontend/dashboard_frontend.html)
- On page load, immediately check `localStorage.getItem('token')`. If missing, redirect to `login_frontend.html`.
- Update `fetch` requests towards the backend API to include the `Authorization: Bearer <token>` header.
- Catch 401 Unauthorized responses to force a redirect to login when the token expires.
- Add a "Logout" button to the header to clear the token and exit.

## Open Questions

> [!WARNING]  
> Are there specific user roles you want to implement right away (e.g., Admin vs User), or is basic authentication for all users sufficient for now?

## Verification Plan

### Automated Tests
- No extensive automated test coverage exists yet, but I will write backend unit tests if requested.
- I will run the FastAPI backend locally to verify that the `python-jose` and `passlib` modules are installed correctly.

### Manual Verification
- Access the `dashboard_frontend.html` directly in the browser; it MUST redirect the user to `login_frontend.html`.
- Attempt to register a user.
- Attempt to login with invalid credentials; observe error.
- Attempt to login with valid credentials; observe successful redirect to dashboard.
- Verify dashboard fetches data correctly using the JWT token and displays it.
- Click 'Logout' and ensure I can no longer view the dashboard page.
