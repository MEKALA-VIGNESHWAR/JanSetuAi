package com.jansetu.repository;

import com.jansetu.entity.UserFeedback;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserFeedbackRepository extends JpaRepository<UserFeedback, Long> {
    List<UserFeedback> findByOpportunityId(Long opportunityId);
    List<UserFeedback> findByStatusOrderByCreatedAtDesc(String status);
    List<UserFeedback> findAllByOrderByCreatedAtDesc();
}
