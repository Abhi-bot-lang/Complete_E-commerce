# Action Plan: Resolving Store API & Connected Errors

This document provides a step-by-step action plan to solve all the existing errors and inconsistencies in your Store API and its connected interfaces (such as Product and Category APIs) so that they work properly.

---

## 1. Identified Errors & Issues

### A. Store Service Code Duplication & Type Inconsistencies
* **Duplicate Imports**: In `app/services/store_service.py`, lines 1-6 are duplicated in lines 9-12.
* **UUID String vs Integer Mismatch**: 
  - In `app/models/store_model.py`, the `Store.id` field is a UUID string:
    `id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))`
  - In `app/services/store_service.py`, functions like `get_store_by_id`, `update_store`, and `delete_store` specify `store_id: int` in their signatures.
  - This is typed incorrectly compared to the actual database model column type and can result in IDE/compiler warnings or incorrect queries.

### B. Missing Authentication (`user_id`) in Store Creation
* In `app/routes/store_routes.py`, `create_store_route` has a hardcoded `user_id = 1`. 
* There is no authentication dependency in use to fetch the logged-in user from the JWT Bearer token, even though `app/utils/JWT.py` exists with JWT verification capabilities.

### C. Critical Runtime Crashes in Product Routes
* In `app/services/product_service.py`, methods require a `user_id` argument to enforce ownership:
  - `create_product(product: ProductCreate, user_id: int, db: Session)`
  - `update_product(product_id: str, data: ProductUpdate, user_id: str, db: Session)`
  - `delete_product(product_id: str, user_id: str, db: Session)`
* In `app/routes/product_routes.py`, the endpoints call these functions **without** passing any `user_id` value!
  - For example: `create_product(product=product, db=db)`
  - This causes immediate **runtime `TypeError: missing 1 required positional argument` crashes** whenever any of these endpoints are hit.

### D. Nested / Double Router Prefix Patterns
* In `app/routes/category.py` and `app/routes/product_routes.py`, router prefixes are declared as `/categories` and `/products`, but the individual routes specify duplicate endpoints like `@router.get("/categories/{category_id}")` or `@router.get("/products")`.
* This yields nested paths such as `/categories/categories/{category_id}` or `/products/products/{product_id}` rather than the clean standard REST resources `/categories/{category_id}` and `/products/{product_id}`.

---

## 2. Step-by-Step Action Plan

### Step 1: Implement `get_current_user` Dependency
We need to leverage your existing `verify_token` function to extract the current authenticated user from the HTTP Authorization headers.
1. Modify `app/dependencies/auth_dependency.py`.
2. Extract the bearer token from the request header using FastAPI's `HTTPBearer`.
3. Decode the JWT token to extract the user email (`sub` claim).
4. Query the database to retrieve the active `User` model, raising a `401 Unauthorized` exception if verification fails.

### Step 2: Clean up and Align Types in Store Service
1. Open `app/services/store_service.py`.
2. Delete the duplicate imports block.
3. Update function parameter annotations for `store_id` from `int` to `str` to perfectly align with the `Store.id` UUID schema.

### Step 3: Inject Authenticated User in Store Routes
1. Open `app/routes/store_routes.py`.
2. Import `Depends` and the newly created `get_current_user` dependency.
3. Remove `user_id = 1` and update the route signature to `current_user: User = Depends(get_current_user)`.
4. Pass `current_user.id` to `create_store`.

### Step 4: Fix Product Routes Runtime Crashes & Path Namespaces
1. Open `app/routes/product_routes.py`.
2. Import `get_current_user` dependency.
3. Fix the nested prefixes by removing duplicate sub-paths:
   - Change `@router.get("/products")` to `@router.get("/")`
   - Change `@router.get("/products/{product_id}")` to `@router.get("/{product_id}")`
   - Change `@router.put("/products/{product_id}")` to `@router.put("/{product_id}")`
   - Change `@router.delete("/products/{product_id}")` to `@router.delete("/{product_id}")`
4. Update endpoint signatures to inject `current_user: User = Depends(get_current_user)`.
5. Pass `current_user.id` into the service methods (`create_product`, `update_product`, `delete_product`).

### Step 5: Fix Category Routes Nested Prefixes
1. Open `app/routes/category.py`.
2. Clean up routing paths to avoid nested prefix paths:
   - Change `@router.get("/categories/{category_id}")` to `@router.get("/{category_id}")`
   - Change `@router.post("/categories")` to `@router.post("/")`
   - Change `@router.put("/categories/{category_id}")` to `@router.put("/{category_id}")`
   - Change `@router.delete("/categories/{category_id}")` to `@router.delete("/{category_id}")`

---

## 3. Verification & Testing Procedure

Once the changes are completed, run the following tests:
1. **FastAPI Docs Check**: Start the app and visit `/docs` (e.g. `http://127.0.0.1:8000/docs`). Verify the structure of the routes is now clean:
   - `/stores/` instead of `/stores/stores/`
   - `/products/` instead of `/products/products/`
   - `/categories/` instead of `/categories/categories/`
2. **User Registration & Login**: Use the register endpoint `/auth/register` and login `/auth/login` to obtain an active token.
3. **Store Testing**: Attempt to create a store using the Bearer token. Verify it successfully resolves without database or authentication errors.
4. **Product CRUD Testing**: Test adding, editing, and deleting a product inside the created store using the token. Ensure there are no runtime argument mismatches.
