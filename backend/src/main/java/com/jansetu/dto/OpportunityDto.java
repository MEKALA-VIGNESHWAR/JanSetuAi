package com.jansetu.dto;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

public class OpportunityDto {
    private Long id;
    private String name;
    private String slug;
    private String description;
    private String shortDescription;

    private String type;
    private String category;
    private String subCategory;

    private String governmentLevel;
    private String state;
    private String districts;

    private String targetGroups;
    private Integer minAge;
    private Integer maxAge;
    private String genderRestriction;

    private String benefits;
    private String benefitType;
    private String benefitAmount;

    private String eligibilitySummary;
    private String requiredDocuments;

    private String applicationUrl;
    private String applicationSteps;
    private String applicationDeadline;

    private String officialSource;
    private String sourceUrl;
    private LocalDate lastVerified;
    private String verificationStatus;

    private String status;
    private String tags;
    private String icon;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    private List<EligibilityRuleDto> eligibilityRules;
    private Boolean isSaved;
    private String applicationStatus;

    public OpportunityDto() {}

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private final OpportunityDto d = new OpportunityDto();

        public Builder id(Long id) { d.id = id; return this; }
        public Builder name(String name) { d.name = name; return this; }
        public Builder slug(String slug) { d.slug = slug; return this; }
        public Builder description(String desc) { d.description = desc; return this; }
        public Builder shortDescription(String desc) { d.shortDescription = desc; return this; }
        public Builder type(String type) { d.type = type; return this; }
        public Builder category(String cat) { d.category = cat; return this; }
        public Builder subCategory(String sub) { d.subCategory = sub; return this; }
        public Builder governmentLevel(String level) { d.governmentLevel = level; return this; }
        public Builder state(String state) { d.state = state; return this; }
        public Builder districts(String dName) { d.districts = dName; return this; }
        public Builder targetGroups(String tg) { d.targetGroups = tg; return this; }
        public Builder minAge(Integer age) { d.minAge = age; return this; }
        public Builder maxAge(Integer age) { d.maxAge = age; return this; }
        public Builder genderRestriction(String gen) { d.genderRestriction = gen; return this; }
        public Builder benefits(String b) { d.benefits = b; return this; }
        public Builder benefitType(String bt) { d.benefitType = bt; return this; }
        public Builder benefitAmount(String ba) { d.benefitAmount = ba; return this; }
        public Builder eligibilitySummary(String es) { d.eligibilitySummary = es; return this; }
        public Builder requiredDocuments(String docs) { d.requiredDocuments = docs; return this; }
        public Builder applicationUrl(String url) { d.applicationUrl = url; return this; }
        public Builder applicationSteps(String steps) { d.applicationSteps = steps; return this; }
        public Builder applicationDeadline(String dl) { d.applicationDeadline = dl; return this; }
        public Builder officialSource(String src) { d.officialSource = src; return this; }
        public Builder sourceUrl(String url) { d.sourceUrl = url; return this; }
        public Builder lastVerified(LocalDate date) { d.lastVerified = date; return this; }
        public Builder verificationStatus(String st) { d.verificationStatus = st; return this; }
        public Builder status(String st) { d.status = st; return this; }
        public Builder tags(String tags) { d.tags = tags; return this; }
        public Builder icon(String icon) { d.icon = icon; return this; }
        public Builder createdAt(LocalDateTime t) { d.createdAt = t; return this; }
        public Builder updatedAt(LocalDateTime t) { d.updatedAt = t; return this; }
        public Builder eligibilityRules(List<EligibilityRuleDto> r) { d.eligibilityRules = r; return this; }
        public Builder isSaved(Boolean saved) { d.isSaved = saved; return this; }
        public Builder applicationStatus(String st) { d.applicationStatus = st; return this; }
        public OpportunityDto build() { return d; }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getSlug() { return slug; }
    public void setSlug(String slug) { this.slug = slug; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getShortDescription() { return shortDescription; }
    public void setShortDescription(String shortDescription) { this.shortDescription = shortDescription; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getSubCategory() { return subCategory; }
    public void setSubCategory(String subCategory) { this.subCategory = subCategory; }
    public String getGovernmentLevel() { return governmentLevel; }
    public void setGovernmentLevel(String governmentLevel) { this.governmentLevel = governmentLevel; }
    public String getState() { return state; }
    public void setState(String state) { this.state = state; }
    public String getDistricts() { return districts; }
    public void setDistricts(String districts) { this.districts = districts; }
    public String getTargetGroups() { return targetGroups; }
    public void setTargetGroups(String targetGroups) { this.targetGroups = targetGroups; }
    public Integer getMinAge() { return minAge; }
    public void setMinAge(Integer minAge) { this.minAge = minAge; }
    public Integer getMaxAge() { return maxAge; }
    public void setMaxAge(Integer maxAge) { this.maxAge = maxAge; }
    public String getGenderRestriction() { return genderRestriction; }
    public void setGenderRestriction(String genderRestriction) { this.genderRestriction = genderRestriction; }
    public String getBenefits() { return benefits; }
    public void setBenefits(String benefits) { this.benefits = benefits; }
    public String getBenefitType() { return benefitType; }
    public void setBenefitType(String benefitType) { this.benefitType = benefitType; }
    public String getBenefitAmount() { return benefitAmount; }
    public void setBenefitAmount(String benefitAmount) { this.benefitAmount = benefitAmount; }
    public String getEligibilitySummary() { return eligibilitySummary; }
    public void setEligibilitySummary(String eligibilitySummary) { this.eligibilitySummary = eligibilitySummary; }
    public String getRequiredDocuments() { return requiredDocuments; }
    public void setRequiredDocuments(String requiredDocuments) { this.requiredDocuments = requiredDocuments; }
    public String getApplicationUrl() { return applicationUrl; }
    public void setApplicationUrl(String applicationUrl) { this.applicationUrl = applicationUrl; }
    public String getApplicationSteps() { return applicationSteps; }
    public void setApplicationSteps(String applicationSteps) { this.applicationSteps = applicationSteps; }
    public String getApplicationDeadline() { return applicationDeadline; }
    public void setApplicationDeadline(String applicationDeadline) { this.applicationDeadline = applicationDeadline; }
    public String getOfficialSource() { return officialSource; }
    public void setOfficialSource(String officialSource) { this.officialSource = officialSource; }
    public String getSourceUrl() { return sourceUrl; }
    public void setSourceUrl(String sourceUrl) { this.sourceUrl = sourceUrl; }
    public LocalDate getLastVerified() { return lastVerified; }
    public void setLastVerified(LocalDate lastVerified) { this.lastVerified = lastVerified; }
    public String getVerificationStatus() { return verificationStatus; }
    public void setVerificationStatus(String verificationStatus) { this.verificationStatus = verificationStatus; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getTags() { return tags; }
    public void setTags(String tags) { this.tags = tags; }
    public String getIcon() { return icon; }
    public void setIcon(String icon) { this.icon = icon; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    public List<EligibilityRuleDto> getEligibilityRules() { return eligibilityRules; }
    public void setEligibilityRules(List<EligibilityRuleDto> eligibilityRules) { this.eligibilityRules = eligibilityRules; }
    public Boolean getIsSaved() { return isSaved; }
    public void setIsSaved(Boolean isSaved) { this.isSaved = isSaved; }
    public String getApplicationStatus() { return applicationStatus; }
    public void setApplicationStatus(String applicationStatus) { this.applicationStatus = applicationStatus; }
}
