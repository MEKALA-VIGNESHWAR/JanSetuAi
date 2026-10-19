package com.jansetu.service;

import com.jansetu.dto.FeedbackDto;
import com.jansetu.entity.Opportunity;
import com.jansetu.entity.User;
import com.jansetu.entity.UserFeedback;
import com.jansetu.repository.OpportunityRepository;
import com.jansetu.repository.UserFeedbackRepository;
import com.jansetu.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class FeedbackService {

    private final UserFeedbackRepository feedbackRepository;
    private final OpportunityRepository opportunityRepository;
    private final UserRepository userRepository;

    public FeedbackService(
            UserFeedbackRepository feedbackRepository,
            OpportunityRepository opportunityRepository,
            UserRepository userRepository) {
        this.feedbackRepository = feedbackRepository;
        this.opportunityRepository = opportunityRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public FeedbackDto submitFeedback(Long userId, FeedbackDto dto) {
        User user = (userId != null) ? userRepository.findById(userId).orElse(null) : null;
        Opportunity opp = (dto.getOpportunityId() != null)
                ? opportunityRepository.findById(dto.getOpportunityId()).orElse(null)
                : null;

        UserFeedback feedback = UserFeedback.builder()
                .user(user)
                .opportunity(opp)
                .feedbackType(dto.getFeedbackType())
                .description(dto.getDescription())
                .status("PENDING")
                .build();

        UserFeedback saved = feedbackRepository.save(feedback);
        return toDto(saved);
    }

    public List<FeedbackDto> getAllFeedback() {
        return feedbackRepository.findAllByOrderByCreatedAtDesc()
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    @Transactional
    public FeedbackDto updateFeedbackStatus(Long id, String status, String adminNotes) {
        UserFeedback feedback = feedbackRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Feedback not found: " + id));

        if (status != null) feedback.setStatus(status.toUpperCase());
        if (adminNotes != null) feedback.setAdminNotes(adminNotes);

        UserFeedback updated = feedbackRepository.save(feedback);
        return toDto(updated);
    }

    private FeedbackDto toDto(UserFeedback f) {
        return FeedbackDto.builder()
                .id(f.getId())
                .userId(f.getUser() != null ? f.getUser().getId() : null)
                .opportunityId(f.getOpportunity() != null ? f.getOpportunity().getId() : null)
                .opportunityName(f.getOpportunity() != null ? f.getOpportunity().getName() : null)
                .feedbackType(f.getFeedbackType())
                .description(f.getDescription())
                .status(f.getStatus())
                .adminNotes(f.getAdminNotes())
                .createdAt(f.getCreatedAt())
                .updatedAt(f.getUpdatedAt())
                .build();
    }
}
