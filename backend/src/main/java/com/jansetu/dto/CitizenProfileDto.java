package com.jansetu.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class CitizenProfileDto {
    private Long id;
    private Long userId;

    // Basic
    private String fullName;
    private Integer age;
    private String gender;
    private String state;
    private String district;
    private String areaType;

    // Education
    private String educationLevel;
    private String courseStream;
    private Boolean isStudent;
    private String collegeType;

    // Occupation
    private String occupation;

    // Economic
    private Integer annualIncome;
    private String incomeCategory;
    private String employmentStatus;

    // Category
    private String socialCategory;
    private Boolean isPwd;
    private String disabilityType;

    // Special conditions
    private String maritalStatus;
    private Boolean isWidow;
    private Boolean isSingleWoman;

    // Farmer
    private Boolean isFarmer;
    private Boolean hasLivestock;
    private Boolean ownsLand;
    private BigDecimal landHoldingAcres;
    private String cropType;

    // Business
    private Boolean hasBusiness;
    private String businessType;

    // Meta & Progress
    private Integer profileCompletion;
    private Integer onboardingStep;
    private String primaryRole;
    private LocalDateTime updatedAt;

    public CitizenProfileDto() {}

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private final CitizenProfileDto d = new CitizenProfileDto();

        public Builder id(Long id) { d.id = id; return this; }
        public Builder userId(Long userId) { d.userId = userId; return this; }
        public Builder fullName(String fullName) { d.fullName = fullName; return this; }
        public Builder age(Integer age) { d.age = age; return this; }
        public Builder gender(String gender) { d.gender = gender; return this; }
        public Builder state(String state) { d.state = state; return this; }
        public Builder district(String district) { d.district = district; return this; }
        public Builder areaType(String areaType) { d.areaType = areaType; return this; }
        public Builder educationLevel(String educationLevel) { d.educationLevel = educationLevel; return this; }
        public Builder courseStream(String courseStream) { d.courseStream = courseStream; return this; }
        public Builder isStudent(Boolean isStudent) { d.isStudent = isStudent; return this; }
        public Builder collegeType(String collegeType) { d.collegeType = collegeType; return this; }
        public Builder occupation(String occupation) { d.occupation = occupation; return this; }
        public Builder annualIncome(Integer annualIncome) { d.annualIncome = annualIncome; return this; }
        public Builder incomeCategory(String incomeCategory) { d.incomeCategory = incomeCategory; return this; }
        public Builder employmentStatus(String employmentStatus) { d.employmentStatus = employmentStatus; return this; }
        public Builder socialCategory(String socialCategory) { d.socialCategory = socialCategory; return this; }
        public Builder isPwd(Boolean isPwd) { d.isPwd = isPwd; return this; }
        public Builder disabilityType(String disabilityType) { d.disabilityType = disabilityType; return this; }
        public Builder maritalStatus(String maritalStatus) { d.maritalStatus = maritalStatus; return this; }
        public Builder isWidow(Boolean isWidow) { d.isWidow = isWidow; return this; }
        public Builder isSingleWoman(Boolean isSingleWoman) { d.isSingleWoman = isSingleWoman; return this; }
        public Builder isFarmer(Boolean isFarmer) { d.isFarmer = isFarmer; return this; }
        public Builder hasLivestock(Boolean hasLivestock) { d.hasLivestock = hasLivestock; return this; }
        public Builder ownsLand(Boolean ownsLand) { d.ownsLand = ownsLand; return this; }
        public Builder landHoldingAcres(BigDecimal acres) { d.landHoldingAcres = acres; return this; }
        public Builder cropType(String cropType) { d.cropType = cropType; return this; }
        public Builder hasBusiness(Boolean hasBusiness) { d.hasBusiness = hasBusiness; return this; }
        public Builder businessType(String businessType) { d.businessType = businessType; return this; }
        public Builder profileCompletion(Integer comp) { d.profileCompletion = comp; return this; }
        public Builder onboardingStep(Integer step) { d.onboardingStep = step; return this; }
        public Builder primaryRole(String role) { d.primaryRole = role; return this; }
        public Builder updatedAt(LocalDateTime time) { d.updatedAt = time; return this; }
        public CitizenProfileDto build() { return d; }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
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
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
