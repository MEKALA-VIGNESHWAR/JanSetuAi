package com.jansetu.dto;

import java.util.ArrayList;
import java.util.List;

public class MatchedOpportunityDto {
    private OpportunityDto opportunity;
    private int matchScore;
    private String matchStatus;
    private boolean isEligible;
    private List<String> passedCriteria = new ArrayList<>();
    private List<String> failedCriteria = new ArrayList<>();
    private List<String> missingFields = new ArrayList<>();

    public MatchedOpportunityDto() {}

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private final MatchedOpportunityDto m = new MatchedOpportunityDto();

        public Builder opportunity(OpportunityDto opp) { m.opportunity = opp; return this; }
        public Builder matchScore(int score) { m.matchScore = score; return this; }
        public Builder matchStatus(String status) { m.matchStatus = status; return this; }
        public Builder isEligible(boolean el) { m.isEligible = el; return this; }
        public Builder passedCriteria(List<String> passed) { m.passedCriteria = passed; return this; }
        public Builder failedCriteria(List<String> failed) { m.failedCriteria = failed; return this; }
        public Builder missingFields(List<String> missing) { m.missingFields = missing; return this; }
        public MatchedOpportunityDto build() { return m; }
    }

    public OpportunityDto getOpportunity() { return opportunity; }
    public void setOpportunity(OpportunityDto opportunity) { this.opportunity = opportunity; }
    public int getMatchScore() { return matchScore; }
    public void setMatchScore(int matchScore) { this.matchScore = matchScore; }
    public String getMatchStatus() { return matchStatus; }
    public void setMatchStatus(String matchStatus) { this.matchStatus = matchStatus; }
    public boolean isEligible() { return isEligible; }
    public void setEligible(boolean eligible) { isEligible = eligible; }
    public List<String> getPassedCriteria() { return passedCriteria; }
    public void setPassedCriteria(List<String> passedCriteria) { this.passedCriteria = passedCriteria; }
    public List<String> getFailedCriteria() { return failedCriteria; }
    public void setFailedCriteria(List<String> failedCriteria) { this.failedCriteria = failedCriteria; }
    public List<String> getMissingFields() { return missingFields; }
    public void setMissingFields(List<String> missingFields) { this.missingFields = missingFields; }
}
