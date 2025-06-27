-- Create primary job queue for the website prospector worker
select * from pgmq.create('worker_jobs'); 