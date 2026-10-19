package com.jansetu.entity;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "saved_opportunities", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"user_id", "opportunity_id"})
})
public class SavedOpportunity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "opportunity_id", nullable = false)
    private Opportunity opportunity;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    public SavedOpportunity() {}

    public SavedOpportunity(User user, Opportunity opportunity) {
        this.user = user;
        this.opportunity = opportunity;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private User user;
        private Opportunity opportunity;

        public Builder user(User user) { this.user = user; return this; }
        public Builder opportunity(Opportunity opportunity) { this.opportunity = opportunity; return this; }
        public SavedOpportunity build() { return new SavedOpportunity(user, opportunity); }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    public Opportunity getOpportunity() { return opportunity; }
    public void setOpportunity(Opportunity opportunity) { this.opportunity = opportunity; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
