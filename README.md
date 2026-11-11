# GhostKey

**Credential lifecycle laboratory · GHOSTKEY · working research prototype**

Model scoped opaque credentials without persisting plaintext bearer tokens.

## Problem and approach

Model scoped opaque credentials without persisting plaintext bearer tokens. This project makes the decision process inspectable through editable scenarios, explicit outputs and reproducible examples. It is an independent repository with a browser application and a Python reference implementation.

## Implemented features

Random token issuance; SHA-256 token lookup; expiry; scope checks; revocation; pairwise HMAC pseudonyms; tokens omitted from reports.

The responsive website runs locally in your browser, accepts editable JSON scenarios, includes preset cases, renders structured results, and exports a JSON report. It has no external runtime dependencies, analytics, external fonts, model API calls or API-key requirement.

## Run the website

Requires Python 3.10+ for the development server. From this directory:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000`. Use **Run analysis** to evaluate the sample; change a scenario and run again. **Export report** downloads the current result. Serve over localhost or HTTPS so Web Crypto is available. Opening `index.html` directly as a file is not supported because the application uses JavaScript modules.

## Command-line usage

```sh
python engine.py sample.json
```

`sample.json` documents the accepted example shape; `expected.json` contains its expected output. `cases.json` adds fixed expected outcomes for boundary and normal cases.

## Tests

Python 3.10+ and Node.js 22+; no package installation:

```sh
python -m unittest -v
node test.mjs
```

The suites check explicit expected outcomes and input immutability. The JavaScript suite also checks malformed top-level inputs and reserved keys. Browser and Python results are compared against the same contract fixtures. Passing these cases is not a security certification or a claim of comprehensive coverage.

## Architecture

| File | Responsibility |
| --- | --- |
| `index.html`, `style.css` | Accessible responsive workbench |
| `app.mjs` | Scenario controls, safe DOM rendering, report export |
| `engine.mjs` | Browser-side algorithm |
| `engine.py` | Independent Python reference and CLI |
| `config.mjs` | Project identity and sample scenarios |
| `cases.json` | Explicit input/output contracts |

Flow: user edits a scenario → JSON parsing and bounded-input checks → project algorithm → text-only result rendering → optional user-triggered report download. There is no application server, account system or backend database.

## Security, privacy and limitations

In-memory educational credential lifecycle, not a production identity provider. Tokens remain temporarily in process memory; restarting loses credentials and the pseudonym key. No password storage, login, TLS, persistence or distributed revocation service.

Scenario data stays in browser memory. The app makes no analysis network requests and stores no inputs in local storage. A hosting provider can still receive ordinary page requests and access logs. Avoid entering real secrets or sensitive evidence; downloaded reports contain your input and results. HTML from scenarios is rendered as text, never executed. Limits cap browser inputs at 100 KB, 1,000 array elements and 15 nesting levels; these limits are prototype safeguards, not a complete denial-of-service defense.

## Development roadmap

- Expand adversarial and boundary fixtures before adding new capabilities.
- Add project-specific form controls alongside the advanced JSON editor.
- Measure performance with published datasets and reproducible methods.
- Conduct independent accessibility and security review.
- Document any integrations before introducing network calls or data retention.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and [LICENSE](LICENSE). Changes should include a concrete failing case and an explanation of assumptions. No benchmark, adoption or certification claims are made without supporting evidence.
