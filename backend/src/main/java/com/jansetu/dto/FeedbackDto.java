package com.jansetu.dto;

import jakarta.validation.constraints.NotBlank;
import java.time.LocalDateTime;

public class FeedbackDto {
    private Long id;
    private Long userId;
    private Long opportunityId;
    private String opportunityName;

    @NotBlank(message = "Feedback type is required")
    private String feedbackType;

    @NotBlank(message = "Description is required")
    private String description;

    private String status;
    private String adminNotes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public FeedbackDto() {}

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private final FeedbackDto d = new FeedbackDto();
        public Builder id(Long id) { d.id = id; return this; }
        public Builder userId(Long uid) { d.userId = uid; return this; }
        public Builder opportunityId(Long oppId) { d.opportunityId = oppId; return this; }
        public Builder opportunityName(String n) { d.opportunityName = n; return this; }
        public Builder feedbackType(String type) { d.feedbackType = type; return this; }
        public Builder description(String desc) { d.description = desc; return this; }
        public Builder status(String s) { d.status = s; return this; }
        public Builder adminNotes(String notes) { d.adminNotes = notes; return this; }
        public Builder createdAt(LocalDateTime t) { d.createdAt = t; return this; }
        public Builder updatedAt(LocalDateTime t) { d.updatedAt = t; return this; }
        public FeedbackDto build() { return d; }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public Long getOpportunityId() { return opportunityId; }
    public void setOpportunityId(Long opportunityId) { this.opportunityId = opportunityId; }
    public String getOpportunityName() { return opportunityName; }
    public void setOpportunityName(String opportunityName) { this.opportunityName = opportunityName; }
    public String getFeedbackType() { return feedbackType; }
    public void setFeedbackType(String feedbackType) { this.feedbackType = feedbackType; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getAdminNotes() { return adminNotes; }
    public void setAdminNotes(String adminNotes) { this.adminNotes = adminNotes; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
