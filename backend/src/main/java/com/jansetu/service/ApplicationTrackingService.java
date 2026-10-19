package com.jansetu.service;

import com.jansetu.dto.ApplicationTrackingDto;
import com.jansetu.entity.ApplicationTracking;
import com.jansetu.entity.Opportunity;
import com.jansetu.entity.User;
import com.jansetu.repository.ApplicationTrackingRepository;
import com.jansetu.repository.OpportunityRepository;
import com.jansetu.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ApplicationTrackingService {

    private final ApplicationTrackingRepository trackingRepository;
    private final OpportunityRepository opportunityRepository;
    private final UserRepository userRepository;

    public ApplicationTrackingService(
            ApplicationTrackingRepository trackingRepository,
            OpportunityRepository opportunityRepository,
            UserRepository userRepository) {
        this.trackingRepository = trackingRepository;
        this.opportunityRepository = opportunityRepository;
        this.userRepository = userRepository;
    }

    public List<ApplicationTrackingDto> getUserTrackings(Long userId) {
        return trackingRepository.findByUserIdOrderByUpdatedAtDesc(userId)
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    @Transactional
    public ApplicationTrackingDto trackOpportunity(Long userId, Long opportunityId, String status, String notes, LocalDate appliedDate) {
        ApplicationTracking tracking = trackingRepository.findByUserIdAndOpportunityId(userId, opportunityId)
                .orElseGet(() -> {
                    User user = userRepository.findById(userId)
                            .orElseThrow(() -> new IllegalArgumentException("User not found: " + userId));
                    Opportunity opp = opportunityRepository.findById(opportunityId)
                            .orElseThrow(() -> new IllegalArgumentException("Opportunity not found: " + opportunityId));
                    return ApplicationTracking.builder()
                            .user(user)
                            .opportunity(opp)
                            .build();
                });

        if (status != null && !status.isBlank()) {
            tracking.setStatus(status.toUpperCase());
        }
        if (notes != null) {
            tracking.setNotes(notes);
        }
        if (appliedDate != null) {
            tracking.setAppliedDate(appliedDate);
        }

        ApplicationTracking saved = trackingRepository.save(tracking);
        return toDto(saved);
    }

    @Transactional
    public void deleteTracking(Long userId, Long trackingId) {
        trackingRepository.findById(trackingId).ifPresent(t -> {
            if (t.getUser().getId().equals(userId)) {
                trackingRepository.delete(t);
            }
        });
    }

    private ApplicationTrackingDto toDto(ApplicationTracking t) {
        return ApplicationTrackingDto.builder()
                .id(t.getId())
                .userId(t.getUser().getId())
                .opportunityId(t.getOpportunity().getId())
                .opportunityName(t.getOpportunity().getName())
                .opportunityCategory(t.getOpportunity().getCategory())
                .opportunityType(t.getOpportunity().getType())
                .applicationUrl(t.getOpportunity().getApplicationUrl())
                .status(t.getStatus())
                .notes(t.getNotes())
                .appliedDate(t.getAppliedDate())
                .createdAt(t.getCreatedAt())
                .updatedAt(t.getUpdatedAt())
                .build();
    }
}
