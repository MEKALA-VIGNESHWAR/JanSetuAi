package com.jansetu.dto;

public class EligibilityRuleDto {
    private Long id;
    private Long opportunityId;
    private String ruleField;
    private String ruleOperator;
    private String ruleValue;
    private Integer ruleGroup;
    private Boolean isMandatory;
    private String description;

    public EligibilityRuleDto() {}

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private final EligibilityRuleDto r = new EligibilityRuleDto();
        public Builder id(Long id) { r.id = id; return this; }
        public Builder opportunityId(Long oppId) { r.opportunityId = oppId; return this; }
        public Builder ruleField(String field) { r.ruleField = field; return this; }
        public Builder ruleOperator(String op) { r.ruleOperator = op; return this; }
        public Builder ruleValue(String val) { r.ruleValue = val; return this; }
        public Builder ruleGroup(Integer group) { r.ruleGroup = group; return this; }
        public Builder isMandatory(Boolean m) { r.isMandatory = m; return this; }
        public Builder description(String d) { r.description = d; return this; }
        public EligibilityRuleDto build() { return r; }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getOpportunityId() { return opportunityId; }
    public void setOpportunityId(Long opportunityId) { this.opportunityId = opportunityId; }
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
}
