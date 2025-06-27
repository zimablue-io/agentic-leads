# Implementation Plan

## 1. Phase 1 — Lead Generation & Qualification

### 1.1 Database & Schema

- Add tables: `performance_audits`, `enrichments`, `outreach_drafts`, `proposals`, `quotes`, `requirements`, `contracts`, `approvals`.
- Extend existing `prospects` row status fields (e.g. `audit_score`, `qualified` boolean).

### 1.2 Workers & Server Actions

- **Performance Audit**: Lighthouse/API → store results in `performance_audits`.
- **Lead Enrichment**: Clearbit (or similar) → write to `enrichments`.
- **Outreach Draft**: GPT-generated personalised email using audit & enrichment data.
- **Proposal & Quote Generators**: Populate `proposals`, `quotes` based on templates + hours estimator.
- **Requirements Intake Handler**: Webhook receiver to persist answers in `requirements`.
- **Contract Generator**: Build PDF/Docx from proposal + scope; save in `contracts`.
- **Client Approval Flow**: Digital-signature provider webhook → mark `approvals` row, transition to Phase 2.

### 1.3 Dashboard UI

- Prospects list & detail (audit scores, enrichment metadata, contacts).
- Proposal / Quote viewer with "Send to client" & "Mark approved".
- Requirements intake status & link sharing.
- Contract preview & signature status.

### 1.4 Realtime & Notifications

- Supabase realtime channels for prospect / proposal status.
- Email (or Slack) notifications on key transitions (audit ready, proposal sent, approval received).

---

## 2. Phase 2 — App Development

### 2.1 Database & Schema

- Tables: `projects`, `project_versions`, `change_requests`, `feedback`, `deployments`.

### 2.2 Workers & Pipelines

- **LLM Scaffolder**: Generate starter repo from requirements (OpenAI function-calling).
- **Component Composer**: Map requested features → reusable UI blocks.
- **Preview Deployment**: Automatic deploy to Vercel; record URL in `deployments`.
- **Change-Management Worker**: Apply approved change requests, update `project_versions`.

### 2.3 Dashboard UI

- Build progress overview (version timeline, deployment status).
- Preview links with password protection.
- Feedback / change request submission & tracking.

### 2.4 Audit & Versioning

- Changelog auto-generation with GPT summaries.
- Logs persisted for compliance / rollback.

---

## 3. Phase 3 — Client Hand-off

### 3.1 Database & Schema

- Tables: `handoffs`, `credentials`, `documentation_links`, `support_requests`.

### 3.2 Automation

- **Hosting Setup**: DNS, SSL, ENV via Infrastructure-as-Code scripts.
- **CI/CD Integration**: Configure GitHub Actions (or alternatives) for auto-deploy.
- **Documentation Generator**: README, technical docs, environment setup.
- **Post-Handoff Agent**: Endpoint for ongoing questions / future change requests.

### 3.3 Dashboard UI

- Final hand-off checklist with downloadable artefacts.
- Credential vault (time-boxed access for client).
- Support request form routing to Post-Handoff agent.

---

## 4. Cross-cutting Concerns

- Authentication & multi-tenant (Supabase Row-Level-Security).
- Secrets & environment configuration management (Dotenv, Vercel / Supabase secrets).
- CI pipelines for Node & Python: type-checks, tests, lint, e2e.
- Observability: structured logging, tracing (OTel), error reporting (Sentry).
- Notification channels: email, Slack, or Discord integration.
- Automated data retention & backups.
