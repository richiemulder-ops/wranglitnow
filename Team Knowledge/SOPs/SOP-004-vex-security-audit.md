# SOP: Security Audit

> **Default owner:** Vex. Any agent can invoke this skill.

Vex's signature workflow for auditing the application surface — credentials, authorization, integrations, data handling — and producing a severity-tagged findings report with proof-of-exploit and fix recommendations.

## When this skill activates

Trigger phrases — invoke this SOP when the user (via Larry) says any of:

- "audit my [app / database / API / integration / vault] for security issues"
- "is this safe to ship?"
- "review my security posture"
- "I'm about to launch / go public — security check"
- "I added a [webhook / integration / endpoint] — is it secure?"
- "I think I have a credential leak"
- "GDPR audit"
- "RLS / authorization audit"

## Procedure

The audit runs in four phases. Don't skip phases — earlier findings change later ones (a leaked service-role key changes the entire RLS audit, for example).

### Phase 1 — Credential hygiene

Before auditing anything else, confirm credentials aren't already leaking. A leaked key makes every other control irrelevant.

1. **Search the codebase for hardcoded secrets.** Grep for patterns: `service_role`, `sk-`, `Bearer `, `api_key`, `apikey`, `secret`, `password`, `client_secret`, common provider prefixes (e.g., `AIza`, `xoxp-`, `xoxb-`, `ghp_`, `pk_live_`, `sk_live_`).
2. **Check committed `.env` files.** If `.env` is in git history, that's CRITICAL — the secret is public, even if the file is now `.gitignore`d.
3. **Check the your Wranglit.** Search `PKM/` and `Team Knowledge/` for anything that looks like a credential. Your Wranglit is markdown content, not a secret store. If credentials are in there, that's CRITICAL.
4. **Check client-side bundles.** If the project ships a frontend, confirm the service-role / admin / write-scoped key is **not** exposed to the browser. Browser-visible keys must be scoped to public/anon roles only.
5. **Check secret-manager hygiene.** Where do secrets actually live? `.env` outside the repo, OS keychain, the platform's secret manager? If the answer is "I email them around," that's a finding.

Output for Phase 1: a list of any credentials found in the wrong place, with severity (CRITICAL for service-role / production keys, HIGH for sandbox / dev keys, MEDIUM for keys with limited scope).

### Phase 2 — Authorization audit

The most common vulnerability in modern apps: a row, route, or object that should require authorization and doesn't.

1. **Enumerate the protected resources.** Database tables, API routes, storage buckets, edge functions, RPC endpoints. What should require auth? What requires it today?
2. **For every database table or row-level resource:**
   - Confirm row-level security (or the equivalent for your platform) is enabled.
   - Confirm at least one well-crafted policy per action (SELECT, INSERT, UPDATE, DELETE).
   - Confirm `auth.uid()` (or your platform's equivalent) is used safely. On Postgres/Supabase specifically, wrap it: `(SELECT auth.uid())` to ensure single evaluation.
   - Confirm there's exactly **one** permissive policy per action, not several stacked. Multiple permissive policies compound and slow queries; consolidating is faster and clearer.
   - Confirm columns referenced in policies are indexed.
3. **For every API route or endpoint:**
   - Is authentication enforced before the handler runs?
   - Is authorization enforced after authentication (does this user have permission for this resource)?
   - Is rate limiting in place?
   - Is CORS scoped to known origins, not `*` for anything authenticated?
4. **For every privileged code path** (SECURITY DEFINER functions in Postgres, admin endpoints, webhook handlers that bypass auth):
   - Audit line by line for parameter injection (string concatenation into SQL or shell).
   - Audit for over-return (does this function return more rows / columns than the caller needs?).
   - Audit for missing access checks (does the function trust its caller, or does it verify?).
   - If it could be SECURITY INVOKER (or its non-privileged equivalent) instead, it must be.
5. **Prove every finding.** Don't report "this looks unsafe." Report: "Running this query as an anonymous user returns 12 rows that should be private. Here is the query. Here is the response."

Output for Phase 2: a list of authorization gaps with proof-of-exploit (the query, the curl, the script) and severity.

### Phase 3 — Integration and surface hardening

For every external surface — APIs you expose, webhooks you receive, third-party integrations you call:

1. **Webhooks you receive:** signature verification, replay protection (event-ID idempotency), timeout-and-retry behavior, error handling that doesn't leak internals.
2. **APIs you call:** credential scope (least privilege on the OAuth scopes / API key permissions), retry with exponential backoff, structured logging that never logs the credential or sensitive payload.
3. **Security headers** on web-facing surfaces: CSP, HSTS, X-Frame-Options or `frame-ancestors`, Referrer-Policy, Permissions-Policy. If you're behind a hosting platform (Vercel, Netlify, Cloudflare), the headers are configured there.
4. **CORS:** scoped to known origins for any authenticated endpoint. `Access-Control-Allow-Origin: *` is a finding on anything that requires auth.
5. **Input validation:** every user-controlled input is validated server-side (not just client-side). Type, length, allowed characters, allowed values.

Output for Phase 3: a list of integration and surface findings with severity.

### Phase 4 — Data-handling and GDPR posture

For applications that store user data, especially PII:

1. **Data minimization:** is the team storing only what it needs? Unused columns, unused tables, abandoned exports.
2. **Encryption at rest:** confirmed for the database and any storage buckets holding PII.
3. **Encryption in transit:** TLS everywhere, including internal service-to-service calls if your topology has them.
4. **Right to erasure:** is there an erasure pipeline? When a user requests deletion, what actually happens? Are there shadow copies (logs, analytics events, backups) that survive the pipeline?
5. **Data portability:** can a user export their own data in a structured format?
6. **Consent management:** if cookies, tracking, or analytics are in play, is consent recorded, scoped, and revocable?
7. **Audit logging:** are admin / privileged operations logged? Who-did-what-when?

Output for Phase 4: a list of data-handling findings with severity. If the user is in GDPR scope, Lex's legal interpretation drives which findings are mandatory; Vex's implementation review confirms the technical controls.

## Findings format

Every finding in the report follows this structure:

```
### [SEVERITY] <Short title>

**Where:** <file path / table name / endpoint / surface>

**What:** <one-paragraph description of the issue>

**Proof-of-exploit:**
<the query, the curl, the script, the screenshot — concrete evidence>

**Fix recommendation:**
<specific, actionable, copy-pasteable where possible>

**Verification step:**
<how to confirm the fix worked — the same test that proved the vulnerability>
```

## Severity ladder

- **CRITICAL** — exploitable now, exposes user data or grants unauthorized access, ship-blocker. Examples: leaked production service-role key, RLS disabled on a PII table, SQL injection in a SECURITY DEFINER function.
- **HIGH** — exploitable with modest effort or specific conditions; should be fixed before next release. Examples: missing rate limiting on auth endpoints, overly broad CORS on authenticated endpoint, missing index on a frequently-checked RLS column.
- **MEDIUM** — partial defense in depth missing; fix during normal cycle. Examples: missing security headers, verbose error responses leaking internals, weaker-than-recommended TLS config.
- **LOW** — hygiene / hardening recommendations; backlog. Examples: log retention longer than necessary, missing CSP report-only directive, minor naming inconsistencies in policy names.

Pad the severity ladder honestly. Inflated severity destroys the team's trust in the gate.

## Output / definition of done

A security audit is done when **all** of these are true:

- [ ] All four phases completed (credential, authorization, integration, data-handling).
- [ ] Every finding has proof-of-exploit, severity, fix recommendation, and a verification step.
- [ ] Report is at `Deliverables/YYYY-MM-DD-<slug>-security-audit.md`.
- [ ] Session-log entry written at `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_vex_<slug>.md` capturing methodology and what to investigate next.
- [ ] No fixes applied without explicit user approval. Vex audits and recommends; the implementing specialist applies after approval.
- [ ] If any CRITICAL findings exist, they are surfaced to the user immediately, not buried at the bottom of the report.

If the audit found CRITICAL issues that block shipping, say so explicitly in the report's verdict line. Don't let urgency get lost.
