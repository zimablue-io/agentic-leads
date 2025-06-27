-- Seed data for audiences
INSERT INTO audiences (name, description, config)
VALUES
  ('local_business', 'Local service-based businesses (plumbers, dentists, etc.) in a specific city.', '{"search_patterns":["{keyword} {location}","{keyword} near me {location}","best {keyword} {location}","{location} {keyword} services"],"keywords":["plumber","electrician","dentist","lawyer","accountant","real estate agent","contractor","auto repair","veterinarian","restaurant","hair salon","fitness gym","chiropractor"],"max_prospects_per_run":25}'::jsonb),
  ('ecommerce', 'Small to mid-size e-commerce stores selling physical products online.', '{"search_patterns":["buy {keyword} online","{keyword} online store","{keyword} shop","{keyword} ecommerce"],"keywords":["jewelry","clothing","electronics","home goods","books","sporting goods","beauty products","pet supplies","toys"],"max_prospects_per_run":20}'::jsonb),
  ('saas', 'B2B SaaS companies offering subscription-based software/services.', '{"search_patterns":["{keyword} software","{keyword} platform","{keyword} solution","{keyword} tools"],"keywords":["project management","crm","accounting","hr","marketing","analytics","communication","design","development"],"max_prospects_per_run":15}'::jsonb)
ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description, config = EXCLUDED.config; 

-- Mock data for initial workflow runs and prospects -------------------------------------

-- Insert two completed workflow runs if they don't already exist
INSERT INTO workflow_runs (audience_id, location, status, started_at, finished_at)
SELECT a.id, 'San Francisco', 'completed', NOW() - INTERVAL '1 day', NOW() - INTERVAL '23 hours'
FROM audiences a
WHERE a.name = 'local_business'
  AND NOT EXISTS (
    SELECT 1 FROM workflow_runs wr WHERE wr.audience_id = a.id AND wr.location = 'San Francisco'
  );

INSERT INTO workflow_runs (audience_id, location, status, started_at, finished_at)
SELECT a.id, 'New York', 'completed', NOW() - INTERVAL '12 hours', NOW() - INTERVAL '11 hours 45 minutes'
FROM audiences a
WHERE a.name = 'ecommerce'
  AND NOT EXISTS (
    SELECT 1 FROM workflow_runs wr WHERE wr.audience_id = a.id AND wr.location = 'New York'
  );

-- Insert sample prospects linked to the above runs -------------------------------------
INSERT INTO prospects (workflow_run_id, url, source_query)
SELECT wr.id, 'https://example-plumber.com', 'plumber san francisco'
FROM workflow_runs wr
JOIN audiences a ON a.id = wr.audience_id
WHERE a.name = 'local_business' AND wr.location = 'San Francisco'
  AND NOT EXISTS (
    SELECT 1 FROM prospects p WHERE p.url = 'https://example-plumber.com'
  );

INSERT INTO prospects (workflow_run_id, url, source_query)
SELECT wr.id, 'https://joes-dentist.com', 'dentist san francisco'
FROM workflow_runs wr
JOIN audiences a ON a.id = wr.audience_id
WHERE a.name = 'local_business' AND wr.location = 'San Francisco'
  AND NOT EXISTS (
    SELECT 1 FROM prospects p WHERE p.url = 'https://joes-dentist.com'
  );

INSERT INTO prospects (workflow_run_id, url, source_query)
SELECT wr.id, 'https://shopelectro.com', 'electronics store new york'
FROM workflow_runs wr
JOIN audiences a ON a.id = wr.audience_id
WHERE a.name = 'ecommerce' AND wr.location = 'New York'
  AND NOT EXISTS (
    SELECT 1 FROM prospects p WHERE p.url = 'https://shopelectro.com'
  );

-- Insert simple site analysis JSON scores for each prospect ----------------------------
INSERT INTO site_analyses (prospect_id, scores_json)
SELECT p.id, '{"performance": 85, "seo": 90, "accessibility": 80}'::jsonb
FROM prospects p
WHERE p.url = 'https://example-plumber.com'
  AND NOT EXISTS (
    SELECT 1 FROM site_analyses sa WHERE sa.prospect_id = p.id
  );

INSERT INTO site_analyses (prospect_id, scores_json)
SELECT p.id, '{"performance": 78, "seo": 72, "accessibility": 88}'::jsonb
FROM prospects p
WHERE p.url = 'https://joes-dentist.com'
  AND NOT EXISTS (
    SELECT 1 FROM site_analyses sa WHERE sa.prospect_id = p.id
  );

INSERT INTO site_analyses (prospect_id, scores_json)
SELECT p.id, '{"performance": 92, "seo": 95, "accessibility": 90}'::jsonb
FROM prospects p
WHERE p.url = 'https://shopelectro.com'
  AND NOT EXISTS (
    SELECT 1 FROM site_analyses sa WHERE sa.prospect_id = p.id
  );

-- Insert contact examples ----------------------------------------------------------------
INSERT INTO contacts (prospect_id, type, value)
SELECT p.id, 'email', 'info@example-plumber.com'
FROM prospects p
WHERE p.url = 'https://example-plumber.com'
  AND NOT EXISTS (
    SELECT 1 FROM contacts c WHERE c.value = 'info@example-plumber.com'
  );

INSERT INTO contacts (prospect_id, type, value)
SELECT p.id, 'phone', '+1-555-123-4567'
FROM prospects p
WHERE p.url = 'https://joes-dentist.com'
  AND NOT EXISTS (
    SELECT 1 FROM contacts c WHERE c.value = '+1-555-123-4567'
  );

INSERT INTO contacts (prospect_id, type, value)
SELECT p.id, 'email', 'support@shopelectro.com'
FROM prospects p
WHERE p.url = 'https://shopelectro.com'
  AND NOT EXISTS (
    SELECT 1 FROM contacts c WHERE c.value = 'support@shopelectro.com'
  ); 