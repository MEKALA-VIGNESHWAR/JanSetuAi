-- JanSetu AI Database Schema
-- ============================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'USER',  -- USER, ADMIN
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Citizen profiles (progressive - fields can be null)
CREATE TABLE IF NOT EXISTS citizen_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Basic
    full_name VARCHAR(255),
    age INTEGER,
    gender VARCHAR(20),          -- MALE, FEMALE, OTHER
    state VARCHAR(100),
    district VARCHAR(100),
    area_type VARCHAR(10),       -- RURAL, URBAN
    
    -- Education
    education_level VARCHAR(50), -- BELOW_10TH, 10TH, 12TH, DIPLOMA, UNDERGRADUATE, POSTGRADUATE, PHD, NONE
    course_stream VARCHAR(100),
    is_student BOOLEAN DEFAULT false,
    college_type VARCHAR(50),    -- GOVERNMENT, PRIVATE, AIDED, DEEMED
    
    -- Occupation
    occupation VARCHAR(50),      -- STUDENT, FARMER, JOB_SEEKER, EMPLOYEE, ENTREPRENEUR, SELF_EMPLOYED, HOMEMAKER, OTHER
    
    -- Economic
    annual_income INTEGER,       -- in INR
    income_category VARCHAR(20), -- BPL, LIG, MIG, HIG
    employment_status VARCHAR(30), -- EMPLOYED, UNEMPLOYED, SELF_EMPLOYED, RETIRED
    
    -- Category
    social_category VARCHAR(10), -- GENERAL, OBC, SC, ST, EWS
    is_pwd BOOLEAN DEFAULT false,
    disability_type VARCHAR(100),
    
    -- Special conditions
    marital_status VARCHAR(20),  -- UNMARRIED, MARRIED, DIVORCED, WIDOWED
    is_widow BOOLEAN DEFAULT false,
    is_single_woman BOOLEAN DEFAULT false,
    
    -- Farmer-specific
    is_farmer BOOLEAN DEFAULT false,
    has_livestock BOOLEAN DEFAULT false,
    owns_land BOOLEAN DEFAULT false,
    land_holding_acres DECIMAL(10,2),
    crop_type VARCHAR(255),
    
    -- Business
    has_business BOOLEAN DEFAULT false,
    business_type VARCHAR(100),
    
    -- Profile completeness
    profile_completion INTEGER DEFAULT 0,
    onboarding_step INTEGER DEFAULT 0,
    primary_role VARCHAR(50),    -- What best describes them
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Opportunities (unified: schemes, scholarships, jobs, training, subsidies, loans)
CREATE TABLE IF NOT EXISTS opportunities (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE,
    description TEXT,
    short_description VARCHAR(500),
    
    -- Classification
    type VARCHAR(30) NOT NULL,       -- SCHEME, SCHOLARSHIP, JOB, SUBSIDY, TRAINING, LOAN, PROGRAM
    category VARCHAR(50),            -- FARMER, STUDENT, JOB_SEEKER, WOMEN, ENTREPRENEUR, GENERAL, SENIOR_CITIZEN, MINORITY
    sub_category VARCHAR(100),
    
    -- Government
    government_level VARCHAR(20),    -- CENTRAL, STATE, DISTRICT
    state VARCHAR(100),              -- null = all india
    districts TEXT,                  -- comma-separated, null = all districts
    
    -- Target
    target_groups TEXT,              -- JSON array
    min_age INTEGER,
    max_age INTEGER,
    gender_restriction VARCHAR(20),  -- ALL, MALE, FEMALE
    
    -- Benefits
    benefits TEXT,
    benefit_type VARCHAR(50),        -- FINANCIAL, SCHOLARSHIP, JOB, TRAINING, SUBSIDY, INSURANCE, HOUSING, EQUIPMENT, LOAN
    benefit_amount VARCHAR(255),
    
    -- Eligibility
    eligibility_summary TEXT,
    
    -- Documents
    required_documents TEXT,         -- JSON array
    
    -- Application
    application_url VARCHAR(1000),
    application_steps TEXT,          -- JSON array
    application_deadline VARCHAR(255),
    
    -- Source & Verification
    official_source VARCHAR(500),
    source_url VARCHAR(1000),
    last_verified DATE,
    verification_status VARCHAR(20) DEFAULT 'VERIFIED',  -- VERIFIED, UNDER_REVIEW, UNVERIFIED
    
    -- Status
    status VARCHAR(20) DEFAULT 'ACTIVE', -- ACTIVE, EXPIRED, UPDATED, SUSPENDED
    
    -- Tags & search
    tags TEXT,                       -- comma-separated
    icon VARCHAR(10),                -- emoji
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Eligibility rules (rule engine)
CREATE TABLE IF NOT EXISTS eligibility_rules (
    id BIGSERIAL PRIMARY KEY,
    opportunity_id BIGINT NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    
    rule_field VARCHAR(100) NOT NULL,     -- profile field name e.g. 'age', 'occupation', 'annual_income'
    rule_operator VARCHAR(20) NOT NULL,   -- EQ, NEQ, GT, GTE, LT, LTE, IN, NOT_IN, CONTAINS, EXISTS, BETWEEN
    rule_value VARCHAR(500) NOT NULL,     -- value to compare against
    rule_group INTEGER DEFAULT 0,         -- group rules with AND within group, OR across groups
    is_mandatory BOOLEAN DEFAULT true,    -- mandatory vs nice-to-have
    description VARCHAR(500),             -- human-readable description
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Saved opportunities
CREATE TABLE IF NOT EXISTS saved_opportunities (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    opportunity_id BIGINT NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, opportunity_id)
);

-- Application tracking
CREATE TABLE IF NOT EXISTS application_tracking (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    opportunity_id BIGINT NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL DEFAULT 'INTERESTED', -- INTERESTED, DOCUMENTS_COLLECTED, APPLIED, UNDER_REVIEW, APPROVED, REJECTED
    notes TEXT,
    applied_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, opportunity_id)
);

-- User feedback / reports
CREATE TABLE IF NOT EXISTS user_feedback (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    opportunity_id BIGINT REFERENCES opportunities(id) ON DELETE CASCADE,
    feedback_type VARCHAR(50) NOT NULL, -- ELIGIBILITY_CHANGED, LINK_BROKEN, SCHEME_INACTIVE, INCORRECT_INFO, OTHER
    description TEXT,
    status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, REVIEWED, RESOLVED, DISMISSED
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_opportunities_type ON opportunities(type);
CREATE INDEX idx_opportunities_category ON opportunities(category);
CREATE INDEX idx_opportunities_status ON opportunities(status);
CREATE INDEX idx_opportunities_state ON opportunities(state);
CREATE INDEX idx_opportunities_govt_level ON opportunities(government_level);
CREATE INDEX idx_eligibility_rules_opp ON eligibility_rules(opportunity_id);
CREATE INDEX idx_saved_user ON saved_opportunities(user_id);
CREATE INDEX idx_tracking_user ON application_tracking(user_id);
CREATE INDEX idx_feedback_status ON user_feedback(status);
CREATE INDEX idx_profiles_occupation ON citizen_profiles(occupation);
CREATE INDEX idx_profiles_state ON citizen_profiles(state);
