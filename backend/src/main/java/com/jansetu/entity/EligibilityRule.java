package com.jansetu.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "eligibility_rules")
public class EligibilityRule {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "opportunity_id", nullable = false)
    @JsonIgnore
    private Opportunity opportunity;

    @Column(name = "rule_field", nullable = false, length = 100)
    private String ruleField;

    @Column(name = "rule_operator", nullable = false, length = 20)
    private String ruleOperator;

    @Column(name = "rule_value", nullable = false, length = 500)
    private String ruleValue;

    @Column(name = "rule_group")
    private Integer ruleGroup = 0;

    @Column(name = "is_mandatory")
    private Boolean isMandatory = true;

    @Column(length = 500)
    private String description;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    public EligibilityRule() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Opportunity getOpportunity() { return opportunity; }
    public void setOpportunity(Opportunity opportunity) { this.opportunity = opportunity; }
    public String getRuleField() { return ruleField; }
    public void setRuleField(String ruleField) { this.ruleField = ruleField; }
    public String getRuleOperator() { return ruleOperator; }
    public void setRuleOperator(String ruleOperator) { this.ruleOperator = ruleOperator; }
    public String getRuleValue() { return ruleValue; }
    public void setRuleValue(String ruleValue) { this.ruleValue = ruleValue; }
    public Integer getRuleGroup() { return ruleGroup; }
    public void setRuleGroup(Integer ruleGroup) { this.ruleGroup = ruleGroup; }
    public Boolean getIsMandatory() { return isMandatory; }
    public void setIsMandatory(Boolean isMandatory) { this.isMandatory = isMandatory; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
