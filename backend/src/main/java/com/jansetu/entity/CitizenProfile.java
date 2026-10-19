package com.jansetu.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "citizen_profiles")
public class CitizenProfile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    @JsonIgnore
    private User user;

    // Basic
    @Column(name = "full_name")
    private String fullName;

    private Integer age;

    @Column(length = 20)
    private String gender;

    @Column(length = 100)
    private String state;

    @Column(length = 100)
    private String district;

    @Column(name = "area_type", length = 10)
    private String areaType;

    // Education
    @Column(name = "education_level", length = 50)
    private String educationLevel;

    @Column(name = "course_stream", length = 100)
    private String courseStream;

    @Column(name = "is_student")
    private Boolean isStudent = false;

    @Column(name = "college_type", length = 50)
    private String collegeType;

    // Occupation
    @Column(length = 50)
    private String occupation;

    // Economic
    @Column(name = "annual_income")
    private Integer annualIncome;

    @Column(name = "income_category", length = 20)
    private String incomeCategory;

    @Column(name = "employment_status", length = 30)
    private String employmentStatus;

    // Category
    @Column(name = "social_category", length = 10)
    private String socialCategory;

    @Column(name = "is_pwd")
    private Boolean isPwd = false;

    @Column(name = "disability_type", length = 100)
    private String disabilityType;

    // Special conditions
    @Column(name = "marital_status", length = 20)
    private String maritalStatus;

    @Column(name = "is_widow")
    private Boolean isWidow = false;

    @Column(name = "is_single_woman")
    private Boolean isSingleWoman = false;

    // Farmer-specific
    @Column(name = "is_farmer")
    private Boolean isFarmer = false;

    @Column(name = "has_livestock")
    private Boolean hasLivestock = false;

    @Column(name = "owns_land")
    private Boolean ownsLand = false;

    @Column(name = "land_holding_acres", precision = 10, scale = 2)
    private BigDecimal landHoldingAcres;

    @Column(name = "crop_type")
    private String cropType;

    // Business
    @Column(name = "has_business")
    private Boolean hasBusiness = false;

    @Column(name = "business_type", length = 100)
    private String businessType;

    // Profile completeness
    @Column(name = "profile_completion")
    private Integer profileCompletion = 0;

    @Column(name = "onboarding_step")
    private Integer onboardingStep = 0;

    @Column(name = "primary_role", length = 50)
    private String primaryRole;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    public CitizenProfile() {}

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private final CitizenProfile p = new CitizenProfile();

        public Builder id(Long id) { p.id = id; return this; }
        public Builder user(User user) { p.user = user; return this; }
        public Builder fullName(String fullName) { p.fullName = fullName; return this; }
        public Builder age(Integer age) { p.age = age; return this; }
        public Builder gender(String gender) { p.gender = gender; return this; }
        public Builder state(String state) { p.state = state; return this; }
        public Builder district(String district) { p.district = district; return this; }
        public Builder areaType(String areaType) { p.areaType = areaType; return this; }
        public Builder educationLevel(String educationLevel) { p.educationLevel = educationLevel; return this; }
        public Builder courseStream(String courseStream) { p.courseStream = courseStream; return this; }
        public Builder isStudent(Boolean isStudent) { p.isStudent = isStudent; return this; }
        public Builder collegeType(String collegeType) { p.collegeType = collegeType; return this; }
        public Builder occupation(String occupation) { p.occupation = occupation; return this; }
        public Builder annualIncome(Integer annualIncome) { p.annualIncome = annualIncome; return this; }
        public Builder incomeCategory(String incomeCategory) { p.incomeCategory = incomeCategory; return this; }
        public Builder employmentStatus(String employmentStatus) { p.employmentStatus = employmentStatus; return this; }
        public Builder socialCategory(String socialCategory) { p.socialCategory = socialCategory; return this; }
        public Builder isPwd(Boolean isPwd) { p.isPwd = isPwd; return this; }
        public Builder disabilityType(String disabilityType) { p.disabilityType = disabilityType; return this; }
        public Builder maritalStatus(String maritalStatus) { p.maritalStatus = maritalStatus; return this; }
        public Builder isWidow(Boolean isWidow) { p.isWidow = isWidow; return this; }
        public Builder isSingleWoman(Boolean isSingleWoman) { p.isSingleWoman = isSingleWoman; return this; }
        public Builder isFarmer(Boolean isFarmer) { p.isFarmer = isFarmer; return this; }
        public Builder hasLivestock(Boolean hasLivestock) { p.hasLivestock = hasLivestock; return this; }
        public Builder ownsLand(Boolean ownsLand) { p.ownsLand = ownsLand; return this; }
        public Builder landHoldingAcres(BigDecimal landHoldingAcres) { p.landHoldingAcres = landHoldingAcres; return this; }
        public Builder cropType(String cropType) { p.cropType = cropType; return this; }
        public Builder hasBusiness(Boolean hasBusiness) { p.hasBusiness = hasBusiness; return this; }
        public Builder businessType(String businessType) { p.businessType = businessType; return this; }
        public Builder profileCompletion(Integer profileCompletion) { p.profileCompletion = profileCompletion; return this; }
        public Builder onboardingStep(Integer onboardingStep) { p.onboardingStep = onboardingStep; return this; }
        public Builder primaryRole(String primaryRole) { p.primaryRole = primaryRole; return this; }
        public CitizenProfile build() { return p; }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public Integer getAge() { return age; }
    public void setAge(Integer age) { this.age = age; }
    public String getGender() { return gender; }
    public void setGender(String gender) { this.gender = gender; }
    public String getState() { return state; }
    public void setState(String state) { this.state = state; }
    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }
    public String getAreaType() { return areaType; }
    public void setAreaType(String areaType) { this.areaType = areaType; }
    public String getEducationLevel() { return educationLevel; }
    public void setEducationLevel(String educationLevel) { this.educationLevel = educationLevel; }
    public String getCourseStream() { return courseStream; }
    public void setCourseStream(String courseStream) { this.courseStream = courseStream; }
    public Boolean getIsStudent() { return isStudent; }
    public void setIsStudent(Boolean isStudent) { this.isStudent = isStudent; }
    public String getCollegeType() { return collegeType; }
    public void setCollegeType(String collegeType) { this.collegeType = collegeType; }
    public String getOccupation() { return occupation; }
    public void setOccupation(String occupation) { this.occupation = occupation; }
    public Integer getAnnualIncome() { return annualIncome; }
    public void setAnnualIncome(Integer annualIncome) { this.annualIncome = annualIncome; }
    public String getIncomeCategory() { return incomeCategory; }
    public void setIncomeCategory(String incomeCategory) { this.incomeCategory = incomeCategory; }
    public String getEmploymentStatus() { return employmentStatus; }
    public void setEmploymentStatus(String employmentStatus) { this.employmentStatus = employmentStatus; }
    public String getSocialCategory() { return socialCategory; }
    public void setSocialCategory(String socialCategory) { this.socialCategory = socialCategory; }
    public Boolean getIsPwd() { return isPwd; }
    public void setIsPwd(Boolean isPwd) { this.isPwd = isPwd; }
    public String getDisabilityType() { return disabilityType; }
    public void setDisabilityType(String disabilityType) { this.disabilityType = disabilityType; }
    public String getMaritalStatus() { return maritalStatus; }
    public void setMaritalStatus(String maritalStatus) { this.maritalStatus = maritalStatus; }
    public Boolean getIsWidow() { return isWidow; }
    public void setIsWidow(Boolean isWidow) { this.isWidow = isWidow; }
    public Boolean getIsSingleWoman() { return isSingleWoman; }
    public void setIsSingleWoman(Boolean isSingleWoman) { this.isSingleWoman = isSingleWoman; }
    public Boolean getIsFarmer() { return isFarmer; }
    public void setIsFarmer(Boolean isFarmer) { this.isFarmer = isFarmer; }
    public Boolean getHasLivestock() { return hasLivestock; }
    public void setHasLivestock(Boolean hasLivestock) { this.hasLivestock = hasLivestock; }
    public Boolean getOwnsLand() { return ownsLand; }
    public void setOwnsLand(Boolean ownsLand) { this.ownsLand = ownsLand; }
    public BigDecimal getLandHoldingAcres() { return landHoldingAcres; }
    public void setLandHoldingAcres(BigDecimal landHoldingAcres) { this.landHoldingAcres = landHoldingAcres; }
    public String getCropType() { return cropType; }
    public void setCropType(String cropType) { this.cropType = cropType; }
    public Boolean getHasBusiness() { return hasBusiness; }
    public void setHasBusiness(Boolean hasBusiness) { this.hasBusiness = hasBusiness; }
    public String getBusinessType() { return businessType; }
    public void setBusinessType(String businessType) { this.businessType = businessType; }
    public Integer getProfileCompletion() { return profileCompletion; }
    public void setProfileCompletion(Integer profileCompletion) { this.profileCompletion = profileCompletion; }
    public Integer getOnboardingStep() { return onboardingStep; }
    public void setOnboardingStep(Integer onboardingStep) { this.onboardingStep = onboardingStep; }
    public String getPrimaryRole() { return primaryRole; }
    public void setPrimaryRole(String primaryRole) { this.primaryRole = primaryRole; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
