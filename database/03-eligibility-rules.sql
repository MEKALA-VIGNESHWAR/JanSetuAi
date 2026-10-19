-- JanSetu AI — Eligibility Rules
-- ============================================================
-- Rule Operators: EQ, NEQ, GT, GTE, LT, LTE, IN, NOT_IN, CONTAINS, EXISTS, BETWEEN
-- Rule Fields map to citizen_profile columns

-- PM-KISAN
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-kisan'), 'is_farmer', 'EQ', 'true', 0, true, 'Must be a farmer'),
((SELECT id FROM opportunities WHERE slug='pm-kisan'), 'owns_land', 'EQ', 'true', 0, true, 'Must own agricultural land'),
((SELECT id FROM opportunities WHERE slug='pm-kisan'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older'),
((SELECT id FROM opportunities WHERE slug='pm-kisan'), 'occupation', 'NEQ', 'EMPLOYEE', 0, false, 'Should not be a government employee');

-- PM Fasal Bima Yojana
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-fasal-bima'), 'is_farmer', 'EQ', 'true', 0, true, 'Must be a farmer'),
((SELECT id FROM opportunities WHERE slug='pm-fasal-bima'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older');

-- Kisan Credit Card
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='kisan-credit-card'), 'is_farmer', 'EQ', 'true', 0, true, 'Must be a farmer'),
((SELECT id FROM opportunities WHERE slug='kisan-credit-card'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older'),
((SELECT id FROM opportunities WHERE slug='kisan-credit-card'), 'age', 'LTE', '75', 0, true, 'Must be 75 years or younger');

-- PM Krishi Sinchai Yojana
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-krishi-sinchai'), 'is_farmer', 'EQ', 'true', 0, true, 'Must be a farmer'),
((SELECT id FROM opportunities WHERE slug='pm-krishi-sinchai'), 'owns_land', 'EQ', 'true', 0, true, 'Must own agricultural land'),
((SELECT id FROM opportunities WHERE slug='pm-krishi-sinchai'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older');

-- PM Kisan MaanDhan
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-kisan-maandhan'), 'is_farmer', 'EQ', 'true', 0, true, 'Must be a farmer'),
((SELECT id FROM opportunities WHERE slug='pm-kisan-maandhan'), 'age', 'GTE', '18', 0, true, 'Must be 18-40 years old'),
((SELECT id FROM opportunities WHERE slug='pm-kisan-maandhan'), 'age', 'LTE', '40', 0, true, 'Must be 18-40 years old'),
((SELECT id FROM opportunities WHERE slug='pm-kisan-maandhan'), 'land_holding_acres', 'LTE', '5', 0, true, 'Land holding should be up to 2 hectares (approx 5 acres)');

-- Central Sector Scholarship
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='central-sector-scholarship'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='central-sector-scholarship'), 'education_level', 'IN', 'UNDERGRADUATE,POSTGRADUATE', 0, true, 'Must be in UG or PG course'),
((SELECT id FROM opportunities WHERE slug='central-sector-scholarship'), 'annual_income', 'LTE', '800000', 0, true, 'Family income must be below ₹8 lakh');

-- Post Matric SC Scholarship
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='post-matric-sc'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='post-matric-sc'), 'social_category', 'EQ', 'SC', 0, true, 'Must be Scheduled Caste'),
((SELECT id FROM opportunities WHERE slug='post-matric-sc'), 'annual_income', 'LTE', '250000', 0, true, 'Family income must be below ₹2.5 lakh');

-- Post Matric ST Scholarship
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='post-matric-st'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='post-matric-st'), 'social_category', 'EQ', 'ST', 0, true, 'Must be Scheduled Tribe'),
((SELECT id FROM opportunities WHERE slug='post-matric-st'), 'annual_income', 'LTE', '250000', 0, true, 'Family income must be below ₹2.5 lakh');

-- Post Matric OBC Scholarship
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='post-matric-obc'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='post-matric-obc'), 'social_category', 'EQ', 'OBC', 0, true, 'Must be Other Backward Class'),
((SELECT id FROM opportunities WHERE slug='post-matric-obc'), 'annual_income', 'LTE', '300000', 0, true, 'Family income must be below ₹3 lakh');

-- PMRF
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-research-fellowship'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='pm-research-fellowship'), 'education_level', 'IN', 'POSTGRADUATE,PHD', 0, true, 'Must be pursuing or completed PG'),
((SELECT id FROM opportunities WHERE slug='pm-research-fellowship'), 'age', 'LTE', '35', 0, false, 'Preferably below 35 years');

-- NMMS
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='nmms'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='nmms'), 'education_level', 'IN', 'BELOW_10TH,10TH', 0, true, 'Must be in Class 8-12'),
((SELECT id FROM opportunities WHERE slug='nmms'), 'annual_income', 'LTE', '350000', 0, true, 'Family income below ₹3.5 lakh');

-- Pragati Scholarship
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pragati-scholarship'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='pragati-scholarship'), 'gender', 'EQ', 'FEMALE', 0, true, 'Must be a girl student'),
((SELECT id FROM opportunities WHERE slug='pragati-scholarship'), 'annual_income', 'LTE', '800000', 0, true, 'Family income below ₹8 lakh'),
((SELECT id FROM opportunities WHERE slug='pragati-scholarship'), 'education_level', 'IN', 'UNDERGRADUATE,DIPLOMA', 0, true, 'Must be in degree/diploma technical course');

-- Saksham Scholarship
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='saksham-scholarship'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='saksham-scholarship'), 'is_pwd', 'EQ', 'true', 0, true, 'Must be a person with disability (40%+)'),
((SELECT id FROM opportunities WHERE slug='saksham-scholarship'), 'annual_income', 'LTE', '800000', 0, true, 'Family income below ₹8 lakh');

-- PM Vidyalaxmi
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-vidyalaxmi'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='pm-vidyalaxmi'), 'education_level', 'IN', 'UNDERGRADUATE,POSTGRADUATE,PHD', 0, true, 'Must be in higher education'),
((SELECT id FROM opportunities WHERE slug='pm-vidyalaxmi'), 'annual_income', 'LTE', '2500000', 0, false, 'Family income ≤₹25 lakh for interest subvention');

-- PMKVY
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pmkvy'), 'age', 'GTE', '15', 0, true, 'Must be 15 years or older'),
((SELECT id FROM opportunities WHERE slug='pmkvy'), 'age', 'LTE', '45', 0, true, 'Must be 45 years or younger'),
((SELECT id FROM opportunities WHERE slug='pmkvy'), 'occupation', 'IN', 'JOB_SEEKER,STUDENT,OTHER', 0, false, 'Primarily for job seekers and unemployed');

-- MGNREGA
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='mgnrega'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older'),
((SELECT id FROM opportunities WHERE slug='mgnrega'), 'area_type', 'EQ', 'RURAL', 0, true, 'Must be from rural area');

-- DDU-GKY
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='ddugky'), 'age', 'GTE', '15', 0, true, 'Must be 15-35 years old'),
((SELECT id FROM opportunities WHERE slug='ddugky'), 'age', 'LTE', '35', 0, true, 'Must be 15-35 years old'),
((SELECT id FROM opportunities WHERE slug='ddugky'), 'area_type', 'EQ', 'RURAL', 0, true, 'Must be from rural area');

-- PM SVANidhi
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-svanidhi'), 'occupation', 'IN', 'SELF_EMPLOYED,OTHER', 0, true, 'Must be a street vendor or self-employed'),
((SELECT id FROM opportunities WHERE slug='pm-svanidhi'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older'),
((SELECT id FROM opportunities WHERE slug='pm-svanidhi'), 'area_type', 'EQ', 'URBAN', 0, false, 'Primarily for urban vendors');

-- Stand-Up India
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='stand-up-india'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older'),
((SELECT id FROM opportunities WHERE slug='stand-up-india'), 'social_category', 'IN', 'SC,ST', 1, true, 'Must be SC/ST OR woman'),
((SELECT id FROM opportunities WHERE slug='stand-up-india'), 'gender', 'EQ', 'FEMALE', 2, true, 'Must be SC/ST OR woman');

-- PM Matru Vandana
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-matru-vandana'), 'gender', 'EQ', 'FEMALE', 0, true, 'Must be a woman'),
((SELECT id FROM opportunities WHERE slug='pm-matru-vandana'), 'age', 'GTE', '19', 0, true, 'Must be 19 years or older');

-- PM Ujjwala Yojana
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-ujjwala'), 'gender', 'EQ', 'FEMALE', 0, true, 'Must be a woman'),
((SELECT id FROM opportunities WHERE slug='pm-ujjwala'), 'income_category', 'IN', 'BPL,LIG', 0, true, 'Must be from BPL or low income household'),
((SELECT id FROM opportunities WHERE slug='pm-ujjwala'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older');

-- PM Mudra Yojana
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-mudra'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older'),
((SELECT id FROM opportunities WHERE slug='pm-mudra'), 'occupation', 'IN', 'ENTREPRENEUR,SELF_EMPLOYED,OTHER', 0, false, 'Primarily for entrepreneurs and self-employed');

-- Startup India
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='startup-india'), 'occupation', 'IN', 'ENTREPRENEUR,SELF_EMPLOYED', 0, true, 'Must be an entrepreneur'),
((SELECT id FROM opportunities WHERE slug='startup-india'), 'has_business', 'EQ', 'true', 0, true, 'Must own or plan a business'),
((SELECT id FROM opportunities WHERE slug='startup-india'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older');

-- PMEGP
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pmegp'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older'),
((SELECT id FROM opportunities WHERE slug='pmegp'), 'education_level', 'IN', 'BELOW_10TH,10TH,12TH,DIPLOMA,UNDERGRADUATE,POSTGRADUATE,PHD', 0, false, '8th pass for projects above ₹10 lakh');

-- Ayushman Bharat
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='ayushman-bharat'), 'income_category', 'IN', 'BPL,LIG', 0, true, 'Must be from BPL or low income family');

-- PMAY
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='pm-awas-yojana'), 'annual_income', 'LTE', '1800000', 0, true, 'Family income must be below ₹18 lakh'),
((SELECT id FROM opportunities WHERE slug='pm-awas-yojana'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older');

-- Atal Pension Yojana
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='atal-pension-yojana'), 'age', 'GTE', '18', 0, true, 'Must be 18-40 years old'),
((SELECT id FROM opportunities WHERE slug='atal-pension-yojana'), 'age', 'LTE', '40', 0, true, 'Must be 18-40 years old'),
((SELECT id FROM opportunities WHERE slug='atal-pension-yojana'), 'occupation', 'IN', 'SELF_EMPLOYED,OTHER,JOB_SEEKER,FARMER', 0, false, 'For unorganized sector workers');

-- Rythu Bandhu
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='rythu-bandhu'), 'is_farmer', 'EQ', 'true', 0, true, 'Must be a farmer'),
((SELECT id FROM opportunities WHERE slug='rythu-bandhu'), 'owns_land', 'EQ', 'true', 0, true, 'Must own agricultural land'),
((SELECT id FROM opportunities WHERE slug='rythu-bandhu'), 'state', 'EQ', 'Telangana', 0, true, 'Must be from Telangana');

-- Rythu Bima
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='rythu-bima'), 'is_farmer', 'EQ', 'true', 0, true, 'Must be a farmer'),
((SELECT id FROM opportunities WHERE slug='rythu-bima'), 'state', 'EQ', 'Telangana', 0, true, 'Must be from Telangana'),
((SELECT id FROM opportunities WHERE slug='rythu-bima'), 'age', 'GTE', '18', 0, true, 'Must be 18-59 years old'),
((SELECT id FROM opportunities WHERE slug='rythu-bima'), 'age', 'LTE', '59', 0, true, 'Must be 18-59 years old');

-- Telangana ePASS
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='telangana-epass'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='telangana-epass'), 'state', 'EQ', 'Telangana', 0, true, 'Must be from Telangana'),
((SELECT id FROM opportunities WHERE slug='telangana-epass'), 'social_category', 'IN', 'SC,ST,OBC', 0, true, 'Must be SC/ST/BC/EBC/Minority'),
((SELECT id FROM opportunities WHERE slug='telangana-epass'), 'annual_income', 'LTE', '200000', 0, true, 'Family income below ₹2 lakh');

-- Kalyana Lakshmi
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='kalyana-lakshmi'), 'gender', 'EQ', 'FEMALE', 0, true, 'Must be a woman'),
((SELECT id FROM opportunities WHERE slug='kalyana-lakshmi'), 'state', 'EQ', 'Telangana', 0, true, 'Must be from Telangana'),
((SELECT id FROM opportunities WHERE slug='kalyana-lakshmi'), 'social_category', 'IN', 'SC,ST,OBC', 0, true, 'Must be SC/ST/BC/Minority'),
((SELECT id FROM opportunities WHERE slug='kalyana-lakshmi'), 'annual_income', 'LTE', '200000', 0, true, 'Family income below ₹2 lakh'),
((SELECT id FROM opportunities WHERE slug='kalyana-lakshmi'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older');

-- Aasara Pensions
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='aasara-pensions'), 'state', 'EQ', 'Telangana', 0, true, 'Must be from Telangana'),
((SELECT id FROM opportunities WHERE slug='aasara-pensions'), 'age', 'GTE', '65', 1, true, 'Age 65+ for old age pension'),
((SELECT id FROM opportunities WHERE slug='aasara-pensions'), 'is_widow', 'EQ', 'true', 2, true, 'Widow pension category'),
((SELECT id FROM opportunities WHERE slug='aasara-pensions'), 'is_pwd', 'EQ', 'true', 3, true, 'Disability pension category');

-- Dalit Bandhu
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='dalit-bandhu'), 'state', 'EQ', 'Telangana', 0, true, 'Must be from Telangana'),
((SELECT id FROM opportunities WHERE slug='dalit-bandhu'), 'social_category', 'EQ', 'SC', 0, true, 'Must be Scheduled Caste'),
((SELECT id FROM opportunities WHERE slug='dalit-bandhu'), 'age', 'GTE', '18', 0, true, 'Must be 18 years or older');

-- T-Hub
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='thub-telangana'), 'occupation', 'IN', 'ENTREPRENEUR,SELF_EMPLOYED', 0, true, 'Must be entrepreneur'),
((SELECT id FROM opportunities WHERE slug='thub-telangana'), 'has_business', 'EQ', 'true', 0, false, 'Should have or plan a startup'),
((SELECT id FROM opportunities WHERE slug='thub-telangana'), 'state', 'EQ', 'Telangana', 0, false, 'Preferably from Telangana/Hyderabad');

-- WE Hub
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='we-hub-telangana'), 'gender', 'EQ', 'FEMALE', 0, true, 'Must be a woman'),
((SELECT id FROM opportunities WHERE slug='we-hub-telangana'), 'occupation', 'IN', 'ENTREPRENEUR,SELF_EMPLOYED', 0, true, 'Must be entrepreneur or self-employed'),
((SELECT id FROM opportunities WHERE slug='we-hub-telangana'), 'state', 'EQ', 'Telangana', 0, false, 'Preferably from Telangana');

-- Telangana Skill Development
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='ts-skill-development'), 'state', 'EQ', 'Telangana', 0, true, 'Must be from Telangana'),
((SELECT id FROM opportunities WHERE slug='ts-skill-development'), 'age', 'GTE', '15', 0, true, 'Must be 15-35 years old'),
((SELECT id FROM opportunities WHERE slug='ts-skill-development'), 'age', 'LTE', '35', 0, true, 'Must be 15-35 years old');

-- CM Overseas Scholarship
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='ts-overseas-scholarship'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='ts-overseas-scholarship'), 'state', 'EQ', 'Telangana', 0, true, 'Must be from Telangana'),
((SELECT id FROM opportunities WHERE slug='ts-overseas-scholarship'), 'social_category', 'IN', 'OBC', 0, true, 'Must be BC/EBC/Minority'),
((SELECT id FROM opportunities WHERE slug='ts-overseas-scholarship'), 'annual_income', 'LTE', '500000', 0, true, 'Family income below ₹5 lakh');

-- INSPIRE Scholarship
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='inspire-scholarship'), 'is_student', 'EQ', 'true', 0, true, 'Must be a student'),
((SELECT id FROM opportunities WHERE slug='inspire-scholarship'), 'education_level', 'IN', 'UNDERGRADUATE,POSTGRADUATE', 0, true, 'Must be in BSc/BS/Int MSc');

-- Sukanya Samriddhi
INSERT INTO eligibility_rules (opportunity_id, rule_field, rule_operator, rule_value, rule_group, is_mandatory, description) VALUES
((SELECT id FROM opportunities WHERE slug='sukanya-samriddhi'), 'gender', 'EQ', 'FEMALE', 0, true, 'For girl children'),
((SELECT id FROM opportunities WHERE slug='sukanya-samriddhi'), 'age', 'LTE', '10', 0, true, 'Girl child must be below 10 years');
