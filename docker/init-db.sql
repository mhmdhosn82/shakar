-- Shakar Store Database Initialization
-- This script runs once when the PostgreSQL container is first created

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pg_trgm for full-text search capabilities
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Set timezone
SET timezone = 'Asia/Tehran';

-- Create database comment
COMMENT ON DATABASE shakar_db IS 'فروشگاه شاکار - Shakar Store Management System';
