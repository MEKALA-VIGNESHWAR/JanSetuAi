package com.jansetu.service;

import com.jansetu.dto.EligibilityRuleDto;
import com.jansetu.dto.MatchedOpportunityDto;
import com.jansetu.dto.OpportunityDto;
import com.jansetu.entity.CitizenProfile;
import com.jansetu.entity.EligibilityRule;
import com.jansetu.entity.Opportunity;
import com.jansetu.repository.EligibilityRuleRepository;
import com.jansetu.repository.OpportunityRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class EligibilityEngineService {

    private static final Logger log = LoggerFactory.getLogger(EligibilityEngineService.class);

    private final OpportunityRepository opportunityRepository;
    private final EligibilityRuleRepository eligibilityRuleRepository;

    public EligibilityEngineService(OpportunityRepository opportunityRepository, EligibilityRuleRepository eligibilityRuleRepository) {
        this.opportunityRepository = opportunityRepository;
        this.eligibilityRuleRepository = eligibilityRuleRepository;
    }

    public List<MatchedOpportunityDto> matchOpportunitiesForCitizen(CitizenProfile profile) {
        List<Opportunity> allOpportunities = opportunityRepository.findByStatus("ACTIVE");
        List<EligibilityRule> allRules = eligibilityRuleRepository.findAll();

        Map<Long, List<EligibilityRule>> rulesByOppId = allRules.stream()
                .collect(Collectors.groupingBy(r -> r.getOpportunity().getId()));

        List<MatchedOpportunityDto> results = new ArrayList<>();

        for (Opportunity opp : allOpportunities) {
            List<EligibilityRule> rules = rulesByOppId.getOrDefault(opp.getId(), Collections.emptyList());
            MatchedOpportunityDto match = evaluate(opp, rules, profile);
            results.add(match);
        }

        // Sort: eligible first, then highest score, then by id
        results.sort((a, b) -> {
            if (a.isEligible() != b.isEligible()) {
                return a.isEligible() ? -1 : 1;
            }
            return Integer.compare(b.getMatchScore(), a.getMatchScore());
        });

        return results;
    }

    public MatchedOpportunityDto evaluate(Opportunity opp, List<EligibilityRule> rules, CitizenProfile profile) {
        List<String> passedCriteria = new ArrayList<>();
        List<String> failedCriteria = new ArrayList<>();
        List<String> missingFields = new ArrayList<>();

        int totalMandatory = 0;
        int passedMandatory = 0;
        int failedMandatory = 0;

        int totalOptional = 0;
        int passedOptional = 0;

        // Base checks from Opportunity table fields (state, age, gender)
        checkBaseOpportunityCriteria(opp, profile, passedCriteria, failedCriteria, missingFields);

        boolean failedBaseCheck = !failedCriteria.isEmpty();

        // Evaluate dynamic EligibilityRules
        for (EligibilityRule rule : rules) {
            boolean isMandatory = Boolean.TRUE.equals(rule.getIsMandatory());
            if (isMandatory) totalMandatory++;
            else totalOptional++;

            RuleEvalResult eval = evaluateRule(rule, profile);

            String desc = (rule.getDescription() != null && !rule.getDescription().isBlank())
                    ? rule.getDescription()
                    : (rule.getRuleField() + " " + rule.getRuleOperator() + " " + rule.getRuleValue());

            if (eval == RuleEvalResult.PASS) {
                if (isMandatory) passedMandatory++;
                else passedOptional++;
                passedCriteria.add(desc);
            } else if (eval == RuleEvalResult.FAIL) {
                if (isMandatory) failedMandatory++;
                failedCriteria.add(desc);
            } else if (eval == RuleEvalResult.MISSING_DATA) {
                missingFields.add(rule.getRuleField());
            }
        }

        // Calculate eligibility & score
        boolean isEligible = !failedBaseCheck && failedMandatory == 0;

        int score = 0;
        if (rules.isEmpty()) {
            score = isEligible ? 90 : 30;
        } else {
            int evaluatedMandatory = passedMandatory + failedMandatory;
            double mandatoryWeight = totalMandatory > 0 ? (double) passedMandatory / totalMandatory : 1.0;
            double optionalWeight = totalOptional > 0 ? (double) passedOptional / totalOptional : 1.0;

            if (isEligible) {
                score = (int) Math.round((mandatoryWeight * 80.0) + (optionalWeight * 20.0));
                if (missingFields.isEmpty() && score < 70) score = 70;
            } else {
                score = Math.max(10, 40 - (failedMandatory * 15));
            }
        }

        score = Math.min(100, Math.max(0, score));

        String matchStatus;
        if (!isEligible) {
            matchStatus = "NOT_ELIGIBLE";
        } else if (score >= 80) {
            matchStatus = "HIGH_MATCH";
        } else if (score >= 50) {
            matchStatus = "MODERATE_MATCH";
        } else {
            matchStatus = "LOW_MATCH";
        }

        OpportunityDto oppDto = toOpportunityDto(opp, rules);

        return MatchedOpportunityDto.builder()
                .opportunity(oppDto)
                .matchScore(score)
                .matchStatus(matchStatus)
                .isEligible(isEligible)
                .passedCriteria(passedCriteria)
                .failedCriteria(failedCriteria)
                .missingFields(missingFields)
                .build();
    }

    private void checkBaseOpportunityCriteria(
            Opportunity opp,
            CitizenProfile profile,
            List<String> passedCriteria,
            List<String> failedCriteria,
            List<String> missingFields) {

        // State restriction
        if (opp.getState() != null && !opp.getState().isBlank() && !opp.getState().equalsIgnoreCase("all india")) {
            if (profile.getState() == null || profile.getState().isBlank()) {
                missingFields.add("state");
            } else if (profile.getState().equalsIgnoreCase(opp.getState())) {
                passedCriteria.add("Applicable for " + opp.getState() + " residents");
            } else {
                failedCriteria.add("Restricted to " + opp.getState() + " (your state: " + profile.getState() + ")");
            }
        }

        // Gender restriction
        if (opp.getGenderRestriction() != null && !opp.getGenderRestriction().equalsIgnoreCase("ALL")) {
            if (profile.getGender() == null || profile.getGender().isBlank()) {
                missingFields.add("gender");
            } else if (profile.getGender().equalsIgnoreCase(opp.getGenderRestriction())) {
                passedCriteria.add("Gender matches requirement (" + opp.getGenderRestriction() + ")");
            } else {
                failedCriteria.add("Reserved for " + opp.getGenderRestriction() + " only");
            }
        }

        // Age bounds
        if (opp.getMinAge() != null || opp.getMaxAge() != null) {
            if (profile.getAge() == null || profile.getAge() <= 0) {
                missingFields.add("age");
            } else {
                int age = profile.getAge();
                boolean minPassed = opp.getMinAge() == null || age >= opp.getMinAge();
                boolean maxPassed = opp.getMaxAge() == null || age <= opp.getMaxAge();

                if (minPassed && maxPassed) {
                    passedCriteria.add("Age " + age + " within eligibility range (" +
                            (opp.getMinAge() != null ? opp.getMinAge() : "Any") + " - " +
                            (opp.getMaxAge() != null ? opp.getMaxAge() : "Any") + " yrs)");
                } else {
                    failedCriteria.add("Age " + age + " outside permitted range (" +
                            (opp.getMinAge() != null ? opp.getMinAge() : "Any") + " - " +
                            (opp.getMaxAge() != null ? opp.getMaxAge() : "Any") + " yrs)");
                }
            }
        }
    }

    private RuleEvalResult evaluateRule(EligibilityRule rule, CitizenProfile profile) {
        String field = rule.getRuleField().toLowerCase().trim();
        String op = rule.getRuleOperator().toUpperCase().trim();
        String targetVal = rule.getRuleValue().trim();

        Object userVal = extractProfileFieldValue(profile, field);
        if (userVal == null) {
            return RuleEvalResult.MISSING_DATA;
        }

        try {
            return evaluateCondition(userVal, op, targetVal);
        } catch (Exception e) {
            log.warn("Rule evaluation error for field {} with operator {}: {}", field, op, e.getMessage());
            return RuleEvalResult.FAIL;
        }
    }

    private RuleEvalResult evaluateCondition(Object userVal, String op, String targetVal) {
        String userStr = userVal.toString().trim();

        switch (op) {
            case "EQ":
                return userStr.equalsIgnoreCase(targetVal) ? RuleEvalResult.PASS : RuleEvalResult.FAIL;

            case "NEQ":
                return !userStr.equalsIgnoreCase(targetVal) ? RuleEvalResult.PASS : RuleEvalResult.FAIL;

            case "CONTAINS":
                return userStr.toLowerCase().contains(targetVal.toLowerCase()) ? RuleEvalResult.PASS : RuleEvalResult.FAIL;

            case "IN": {
                List<String> validList = Arrays.stream(targetVal.split(","))
                        .map(s -> s.trim().toLowerCase())
                        .collect(Collectors.toList());
                return validList.contains(userStr.toLowerCase()) ? RuleEvalResult.PASS : RuleEvalResult.FAIL;
            }

            case "NOT_IN": {
                List<String> forbidden = Arrays.stream(targetVal.split(","))
                        .map(s -> s.trim().toLowerCase())
                        .collect(Collectors.toList());
                return !forbidden.contains(userStr.toLowerCase()) ? RuleEvalResult.PASS : RuleEvalResult.FAIL;
            }

            case "GT":
            case "GTE":
            case "LT":
            case "LTE": {
                double userNum = parseNumber(userVal);
                double targetNum = Double.parseDouble(targetVal);
                boolean pass = switch (op) {
                    case "GT" -> userNum > targetNum;
                    case "GTE" -> userNum >= targetNum;
                    case "LT" -> userNum < targetNum;
                    case "LTE" -> userNum <= targetNum;
                    default -> false;
                };
                return pass ? RuleEvalResult.PASS : RuleEvalResult.FAIL;
            }

            case "BETWEEN": {
                String[] parts = targetVal.contains("-") ? targetVal.split("-") : targetVal.split(",");
                if (parts.length == 2) {
                    double userNum = parseNumber(userVal);
                    double min = Double.parseDouble(parts[0].trim());
                    double max = Double.parseDouble(parts[1].trim());
                    return (userNum >= min && userNum <= max) ? RuleEvalResult.PASS : RuleEvalResult.FAIL;
                }
                return RuleEvalResult.FAIL;
            }

            case "EXISTS":
                return !userStr.isBlank() ? RuleEvalResult.PASS : RuleEvalResult.FAIL;

            default:
                return RuleEvalResult.FAIL;
        }
    }

    private double parseNumber(Object val) {
        if (val instanceof Number num) return num.doubleValue();
        return Double.parseDouble(val.toString());
    }

    private Object extractProfileFieldValue(CitizenProfile p, String field) {
        return switch (field) {
            case "age" -> p.getAge();
            case "gender" -> p.getGender();
            case "state" -> p.getState();
            case "district" -> p.getDistrict();
            case "area_type", "areatype" -> p.getAreaType();
            case "education_level", "educationlevel" -> p.getEducationLevel();
            case "course_stream", "coursestream" -> p.getCourseStream();
            case "is_student", "isstudent" -> p.getIsStudent();
            case "college_type", "collegetype" -> p.getCollegeType();
            case "occupation" -> p.getOccupation();
            case "annual_income", "annualincome", "income" -> p.getAnnualIncome();
            case "income_category", "incomecategory" -> p.getIncomeCategory();
            case "employment_status", "employmentstatus" -> p.getEmploymentStatus();
            case "social_category", "socialcategory", "category" -> p.getSocialCategory();
            case "is_pwd", "ispwd" -> p.getIsPwd();
            case "disability_type", "disabilitytype" -> p.getDisabilityType();
            case "marital_status", "maritalstatus" -> p.getMaritalStatus();
            case "is_widow", "iswidow" -> p.getIsWidow();
            case "is_single_woman", "issinglewoman" -> p.getIsSingleWoman();
            case "is_farmer", "isfarmer" -> p.getIsFarmer();
            case "has_livestock", "haslivestock" -> p.getHasLivestock();
            case "owns_land", "ownsland" -> p.getOwnsLand();
            case "land_holding_acres", "landholdingacres" -> p.getLandHoldingAcres();
            case "crop_type", "croptype" -> p.getCropType();
            case "has_business", "hasbusiness" -> p.getHasBusiness();
            case "business_type", "businesstype" -> p.getBusinessType();
            default -> null;
        };
    }

    private OpportunityDto toOpportunityDto(Opportunity o, List<EligibilityRule> rules) {
        List<EligibilityRuleDto> ruleDtos = rules.stream().map(r -> EligibilityRuleDto.builder()
                .id(r.getId())
                .opportunityId(o.getId())
                .ruleField(r.getRuleField())
                .ruleOperator(r.getRuleOperator())
                .ruleValue(r.getRuleValue())
                .ruleGroup(r.getRuleGroup())
                .isMandatory(r.getIsMandatory())
                .description(r.getDescription())
                .build()).collect(Collectors.toList());

        return OpportunityDto.builder()
                .id(o.getId())
                .name(o.getName())
                .slug(o.getSlug())
                .description(o.getDescription())
                .shortDescription(o.getShortDescription())
                .type(o.getType())
                .category(o.getCategory())
                .subCategory(o.getSubCategory())
                .governmentLevel(o.getGovernmentLevel())
                .state(o.getState())
                .districts(o.getDistricts())
                .targetGroups(o.getTargetGroups())
                .minAge(o.getMinAge())
                .maxAge(o.getMaxAge())
                .genderRestriction(o.getGenderRestriction())
                .benefits(o.getBenefits())
                .benefitType(o.getBenefitType())
                .benefitAmount(o.getBenefitAmount())
                .eligibilitySummary(o.getEligibilitySummary())
                .requiredDocuments(o.getRequiredDocuments())
                .applicationUrl(o.getApplicationUrl())
                .applicationSteps(o.getApplicationSteps())
                .applicationDeadline(o.getApplicationDeadline())
                .officialSource(o.getOfficialSource())
                .sourceUrl(o.getSourceUrl())
                .lastVerified(o.getLastVerified())
                .verificationStatus(o.getVerificationStatus())
                .status(o.getStatus())
                .tags(o.getTags())
                .icon(o.getIcon())
                .createdAt(o.getCreatedAt())
                .updatedAt(o.getUpdatedAt())
                .eligibilityRules(ruleDtos)
                .build();
    }

    private enum RuleEvalResult {
        PASS,
        FAIL,
        MISSING_DATA
    }
}
