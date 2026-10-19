package com.jansetu.entity;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.UpdateTimestamp;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;

@Entity
@Table(name = "user_feedback")
public class UserFeedback {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "opportunity_id")
    private Opportunity opportunity;

    @Column(name = "feedback_type", nullable = false, length = 50)
    private String feedbackType;

    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String description;

    @Column(length = 20)
    private String status = "PENDING";

    @Column(name = "admin_notes")
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String adminNotes;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    public UserFeedback() {}

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private final UserFeedback f = new UserFeedback();

        public Builder id(Long id) { f.id = id; return this; }
        public Builder user(User user) { f.user = user; return this; }
        public Builder opportunity(Opportunity opp) { f.opportunity = opp; return this; }
        public Builder feedbackType(String type) { f.feedbackType = type; return this; }
        public Builder description(String desc) { f.description = desc; return this; }
        public Builder status(String status) { f.status = status; return this; }
        public Builder adminNotes(String notes) { f.adminNotes = notes; return this; }
        public UserFeedback build() { return f; }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    public Opportunity getOpportunity() { return opportunity; }
    public void setOpportunity(Opportunity opportunity) { this.opportunity = opportunity; }
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
