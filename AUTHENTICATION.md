# Authentication and credential flow

GHOSTKEY is a local credential-lifecycle demonstration. The website itself has no user login or authenticated backend. Every visitor runs an isolated scenario in their own browser memory.

## Components

| Component | Code | Responsibility |
| --- | --- | --- |
| Workbench | `app.mjs` | Parse the scenario, call the engine, render text, export a report |
| Browser vault | `engine.mjs`, `analyze()` | Issue, check and revoke temporary credentials |
| Python vault | `engine.py`, `CredentialVault` | Reference implementation with issue, verify, revoke and pseudonym methods |
| Contract fixtures | `cases.json`, `test.mjs`, `test_engine.py` | Check expected lifecycle decisions |

## Flow

1. A scenario contains ordered `issue`, `check` and `revoke` events. These are simulation inputs, not authenticated HTTP requests.
2. On `issue`, the browser creates 32 random bytes using Web Crypto. Python uses `secrets.token_urlsafe(32)`. Their string encodings differ; both draw 256 bits of randomness.
3. A SHA-256 digest indexes the credential record. The record contains a pseudonymous subject, audience, permitted scopes, expiry and revocation flag. It does not contain the plaintext token.
4. The scenario runner temporarily holds token strings in a separate in-memory map so later sample events can reference them by a demonstration ID. That is why this is a simulation, not a secret vault for real users.
5. A `check` hashes the token and looks up its record. Access requires a matching audience, an allowed scope, `now < expires`, and an unrevoked record. Unknown tokens deny access.
6. A `revoke` marks the matching record revoked. Subsequent checks deny it. Starting another analysis creates a new vault with no prior credentials.

## Pseudonyms and keys

Each analysis generates an ephemeral 256-bit HMAC key. HMAC-SHA-256 over the subject/audience pair produces a pairwise pseudonym. Changing the audience changes the pseudonym; running a new analysis generates a new key. Keys and raw tokens are omitted from output. They still exist temporarily in process memory.

## What is not implemented

No passwords, cookies, JWTs, refresh tokens, OAuth provider, database, real user verification, rate limiting or distributed revocation. Scenario fields such as subject, time and scope are user controlled. A production service would have to establish those values from trusted authenticated requests, protect keys in an appropriate secret store, and enforce checks on the server. The browser demonstration must never be used as a production authorization boundary.

## Data handling

The application does not send scenario data to a model or analysis API and does not store it in local storage. Exported reports include the scenario inputs and decisions. Use synthetic subjects and avoid actual credentials. GitHub Pages serves public source files and may retain ordinary hosting access logs.
