# Phases

## Phase 1: Lead Generation & Qualification

**Goal**: Identify potential clients, qualify them, and formalize scope.

**Workflows**:

- **Website Prospector** (✅): Scan businesses for online presence.

- **Performance Audit**: Use Lighthouse/API to generate 3rd-party performance report (e.g., site speed, SEO). Acts as neutral “proof.”

- **Lead Enrichment**: Use tools like Clearbit to collect metadata.

- **Outreach Generation**: Personalized pitch referencing audit findings.

- **Proposal Generation**: Auto-filled templates including audit highlights, potential ROI, and offer.

- **Quote Estimation**: Based on estimated hours/features.

- **Requirements Gathering**: Smart intake form (e.g., Typeform + webhook) capturing goals, integrations, pages, features.

- **Contract Generation**: Auto-generate agreement including:
    - Deliverables

    - Exclusions

    - Timeline

    - Budget

    - Change request terms

- **Client Approval**: Digital signature on proposal + contract to move forward.

**Artifacts**:

- CRM entry

- Lighthouse report

- Signed proposal + contract

- Requirements spec

## Phase 2: App Development

**Goal**: Translate requirements into a live, testable application.

**Workflows**:

- **LLM-Powered Scaffolding**: Auto-generate starter code from spec.

- **Component Composition**: Match requested features to reusable UI blocks.

- **Preview Deployment**: Push to Vercel/Netlify with live link.

- **Client Feedback Loop**: Comments or change requests via dashboard or email.

- **Change Management**: Only approved, contract-compliant changes applied.

- **Versioning & Logs**: Each change is logged with rationale (can be GPT-summarized).

**Artifacts**:

- Preview environment

- Source repo

- Feedback/change history

## Phase 3: Client Hand-off

**Goal**: Finalize, host, and transfer control to the client.

**Workflows**:

- **Hosting Setup**: Domain, DNS, SSL, ENV vars.

- **CI/CD Integration**: GitHub Actions or similar for auto-deploy.

- **Client Handoff**: Provide credentials, admin access, training session (optional).

- **Documentation**: README, technical doc, usage instructions, support links.

- **Post-Handoff Agent**: On-demand agent for future changes, questions, or troubleshooting.

**Artifacts**:

- Live production URL

- Source + infra access

- Project documentation
