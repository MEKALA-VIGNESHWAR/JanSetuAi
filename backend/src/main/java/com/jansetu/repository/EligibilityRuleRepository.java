package com.jansetu.repository;

import com.jansetu.entity.EligibilityRule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface EligibilityRuleRepository extends JpaRepository<EligibilityRule, Long> {
    List<EligibilityRule> findByOpportunityId(Long opportunityId);
    List<EligibilityRule> findByOpportunityIdIn(List<Long> opportunityIds);
}
