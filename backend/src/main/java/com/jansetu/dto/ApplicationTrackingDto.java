package com.jansetu.dto;

import java.time.LocalDate;
import java.time.LocalDateTime;

public class ApplicationTrackingDto {
    private Long id;
    private Long userId;
    private Long opportunityId;
    private String opportunityName;
    private String opportunityCategory;
    private String opportunityType;
    private String applicationUrl;
    private String status;
    private String notes;
    private LocalDate appliedDate;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public ApplicationTrackingDto() {}

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private final ApplicationTrackingDto d = new ApplicationTrackingDto();

        public Builder id(Long id) { d.id = id; return this; }
        public Builder userId(Long userId) { d.userId = userId; return this; }
        public Builder opportunityId(Long oppId) { d.opportunityId = oppId; return this; }
        public Builder opportunityName(String name) { d.opportunityName = name; return this; }
        public Builder opportunityCategory(String cat) { d.opportunityCategory = cat; return this; }
        public Builder opportunityType(String t) { d.opportunityType = t; return this; }
        public Builder applicationUrl(String url) { d.applicationUrl = url; return this; }
        public Builder status(String s) { d.status = s; return this; }
        public Builder notes(String notes) { d.notes = notes; return this; }
        public Builder appliedDate(LocalDate dte) { d.appliedDate = dte; return this; }
        public Builder createdAt(LocalDateTime t) { d.createdAt = t; return this; }
        public Builder updatedAt(LocalDateTime t) { d.updatedAt = t; return this; }
        public ApplicationTrackingDto build() { return d; }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public Long getOpportunityId() { return opportunityId; }
    public void setOpportunityId(Long opportunityId) { this.opportunityId = opportunityId; }
    public String getOpportunityName() { return opportunityName; }
    public void setOpportunityName(String opportunityName) { this.opportunityName = opportunityName; }
    public String getOpportunityCategory() { return opportunityCategory; }
    public void setOpportunityCategory(String opportunityCategory) { this.opportunityCategory = opportunityCategory; }
    public String getOpportunityType() { return opportunityType; }
    public void setOpportunityType(String opportunityType) { this.opportunityType = opportunityType; }
    public String getApplicationUrl() { return applicationUrl; }
    public void setApplicationUrl(String applicationUrl) { this.applicationUrl = applicationUrl; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public LocalDate getAppliedDate() { return appliedDate; }
    public void setAppliedDate(LocalDate appliedDate) { this.appliedDate = appliedDate; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
