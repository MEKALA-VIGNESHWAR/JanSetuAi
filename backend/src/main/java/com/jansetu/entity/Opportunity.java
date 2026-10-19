package com.jansetu.entity;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.UpdateTimestamp;
import org.hibernate.type.SqlTypes;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "opportunities")
public class Opportunity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 500)
    private String name;

    @Column(length = 500, unique = true)
    private String slug;

    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String description;

    @Column(name = "short_description", length = 500)
    private String shortDescription;

    // Classification
    @Column(nullable = false, length = 30)
    private String type;

    @Column(length = 50)
    private String category;

    @Column(name = "sub_category", length = 100)
    private String subCategory;

    // Government
    @Column(name = "government_level", length = 20)
    private String governmentLevel;

    @Column(length = 100)
    private String state;

    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String districts;

    // Target
    @Column(name = "target_groups")
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String targetGroups;

    @Column(name = "min_age")
    private Integer minAge;

    @Column(name = "max_age")
    private Integer maxAge;

    @Column(name = "gender_restriction", length = 20)
    private String genderRestriction;

    // Benefits
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String benefits;

    @Column(name = "benefit_type", length = 50)
    private String benefitType;

    @Column(name = "benefit_amount", length = 255)
    private String benefitAmount;

    // Eligibility
    @Column(name = "eligibility_summary")
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String eligibilitySummary;

    // Documents
    @Column(name = "required_documents")
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String requiredDocuments;

    // Application
    @Column(name = "application_url", length = 1000)
    private String applicationUrl;

    @Column(name = "application_steps")
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String applicationSteps;

    @Column(name = "application_deadline", length = 255)
    private String applicationDeadline;

    // Source & Verification
    @Column(name = "official_source", length = 500)
    private String officialSource;

    @Column(name = "source_url", length = 1000)
    private String sourceUrl;

    @Column(name = "last_verified")
    private LocalDate lastVerified;

    @Column(name = "verification_status", length = 20)
    private String verificationStatus = "VERIFIED";

    // Status
    @Column(length = 20)
    private String status = "ACTIVE";

    // Tags & search
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String tags;

    @Column(length = 10)
    private String icon;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @OneToMany(mappedBy = "opportunity", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    private List<EligibilityRule> eligibilityRules = new ArrayList<>();

    public Opportunity() {}

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
    public List<EligibilityRule> getEligibilityRules() { return eligibilityRules; }
    public void setEligibilityRules(List<EligibilityRule> eligibilityRules) { this.eligibilityRules = eligibilityRules; }
}
