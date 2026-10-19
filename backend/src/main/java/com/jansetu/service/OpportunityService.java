package com.jansetu.service;

import com.jansetu.dto.EligibilityRuleDto;
import com.jansetu.dto.OpportunityDto;
import com.jansetu.entity.Opportunity;
import com.jansetu.repository.ApplicationTrackingRepository;
import com.jansetu.repository.EligibilityRuleRepository;
import com.jansetu.repository.OpportunityRepository;
import com.jansetu.repository.SavedOpportunityRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class OpportunityService {

    private final OpportunityRepository opportunityRepository;
    private final EligibilityRuleRepository eligibilityRuleRepository;
    private final SavedOpportunityRepository savedOpportunityRepository;
    private final ApplicationTrackingRepository applicationTrackingRepository;

    public OpportunityService(
            OpportunityRepository opportunityRepository,
            EligibilityRuleRepository eligibilityRuleRepository,
            SavedOpportunityRepository savedOpportunityRepository,
            ApplicationTrackingRepository applicationTrackingRepository) {
        this.opportunityRepository = opportunityRepository;
        this.eligibilityRuleRepository = eligibilityRuleRepository;
        this.savedOpportunityRepository = savedOpportunityRepository;
        this.applicationTrackingRepository = applicationTrackingRepository;
    }

    public Page<OpportunityDto> getOpportunities(
            String category,
            String type,
            String govtLevel,
            String state,
            String search,
            Pageable pageable,
            Long currentUserId) {

        String cleanCategory = (category != null && !category.isBlank() && !category.equalsIgnoreCase("ALL")) ? category.toLowerCase().trim() : null;
        String cleanType = (type != null && !type.isBlank() && !type.equalsIgnoreCase("ALL")) ? type.toLowerCase().trim() : null;
        String cleanGovtLevel = (govtLevel != null && !govtLevel.isBlank() && !govtLevel.equalsIgnoreCase("ALL")) ? govtLevel.toLowerCase().trim() : null;
        String cleanState = (state != null && !state.isBlank() && !state.equalsIgnoreCase("ALL")) ? state.toLowerCase().trim() : null;
        String cleanSearch = (search != null && !search.isBlank()) ? ("%" + search.toLowerCase().trim() + "%") : null;

        Page<Opportunity> page = opportunityRepository.findWithFilters(
                cleanCategory, cleanType, cleanGovtLevel, cleanState, cleanSearch, pageable
        );

        return page.map(opp -> mapToDto(opp, currentUserId));
    }

    public OpportunityDto getOpportunityById(Long id, Long currentUserId) {
        Opportunity opp = opportunityRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Opportunity not found with id: " + id));
        return mapToDto(opp, currentUserId);
    }

    public OpportunityDto getOpportunityBySlug(String slug, Long currentUserId) {
        Opportunity opp = opportunityRepository.findBySlug(slug)
                .orElseThrow(() -> new IllegalArgumentException("Opportunity not found with slug: " + slug));
        return mapToDto(opp, currentUserId);
    }

    public List<String> getCategories() {
        return opportunityRepository.findDistinctCategories();
    }

    public List<String> getTypes() {
        return opportunityRepository.findDistinctTypes();
    }

    public List<String> getStates() {
        return opportunityRepository.findDistinctStates();
    }

    public Map<String, Object> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalActiveSchemes", opportunityRepository.countActive());
        stats.put("totalCategories", opportunityRepository.findDistinctCategories().size());
        stats.put("totalStatesCovered", opportunityRepository.findDistinctStates().size());
        return stats;
    }

    public OpportunityDto mapToDto(Opportunity o, Long currentUserId) {
        List<EligibilityRuleDto> rules = eligibilityRuleRepository.findByOpportunityId(o.getId())
                .stream()
                .map(r -> EligibilityRuleDto.builder()
                        .id(r.getId())
                        .opportunityId(o.getId())
                        .ruleField(r.getRuleField())
                        .ruleOperator(r.getRuleOperator())
                        .ruleValue(r.getRuleValue())
                        .ruleGroup(r.getRuleGroup())
                        .isMandatory(r.getIsMandatory())
                        .description(r.getDescription())
                        .build())
                .collect(Collectors.toList());

        boolean isSaved = false;
        String applicationStatus = null;

        if (currentUserId != null) {
            isSaved = savedOpportunityRepository.existsByUserIdAndOpportunityId(currentUserId, o.getId());
            applicationStatus = applicationTrackingRepository.findByUserIdAndOpportunityId(currentUserId, o.getId())
                    .map(t -> t.getStatus())
                    .orElse(null);
        }

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
                .eligibilityRules(rules)
                .isSaved(isSaved)
                .applicationStatus(applicationStatus)
                .build();
    }
}
