package com.jansetu.entity;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.UpdateTimestamp;
import org.hibernate.type.SqlTypes;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "application_tracking", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"user_id", "opportunity_id"})
})
public class ApplicationTracking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "opportunity_id", nullable = false)
    private Opportunity opportunity;

    @Column(nullable = false, length = 30)
    private String status = "INTERESTED";

    @JdbcTypeCode(SqlTypes.VARCHAR)
    private String notes;

    @Column(name = "applied_date")
    private LocalDate appliedDate;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    public ApplicationTracking() {}

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private final ApplicationTracking at = new ApplicationTracking();

        public Builder id(Long id) { at.id = id; return this; }
        public Builder user(User user) { at.user = user; return this; }
        public Builder opportunity(Opportunity opp) { at.opportunity = opp; return this; }
        public Builder status(String status) { at.status = status; return this; }
        public Builder notes(String notes) { at.notes = notes; return this; }
        public Builder appliedDate(LocalDate date) { at.appliedDate = date; return this; }
        public ApplicationTracking build() { return at; }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    public Opportunity getOpportunity() { return opportunity; }
    public void setOpportunity(Opportunity opportunity) { this.opportunity = opportunity; }
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
