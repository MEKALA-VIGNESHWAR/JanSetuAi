package com.jansetu.service;

import com.jansetu.dto.OpportunityDto;
import com.jansetu.entity.Opportunity;
import com.jansetu.entity.SavedOpportunity;
import com.jansetu.entity.User;
import com.jansetu.repository.OpportunityRepository;
import com.jansetu.repository.SavedOpportunityRepository;
import com.jansetu.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class SavedOpportunityService {

    private final SavedOpportunityRepository savedOpportunityRepository;
    private final OpportunityRepository opportunityRepository;
    private final UserRepository userRepository;
    private final OpportunityService opportunityService;

    public SavedOpportunityService(
            SavedOpportunityRepository savedOpportunityRepository,
            OpportunityRepository opportunityRepository,
            UserRepository userRepository,
            OpportunityService opportunityService) {
        this.savedOpportunityRepository = savedOpportunityRepository;
        this.opportunityRepository = opportunityRepository;
        this.userRepository = userRepository;
        this.opportunityService = opportunityService;
    }

    @Transactional
    public void saveOpportunity(Long userId, Long opportunityId) {
        if (savedOpportunityRepository.existsByUserIdAndOpportunityId(userId, opportunityId)) {
            return;
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found: " + userId));
        Opportunity opp = opportunityRepository.findById(opportunityId)
                .orElseThrow(() -> new IllegalArgumentException("Opportunity not found: " + opportunityId));

        SavedOpportunity saved = SavedOpportunity.builder()
                .user(user)
                .opportunity(opp)
                .build();
        savedOpportunityRepository.save(saved);
    }

    @Transactional
    public void unsaveOpportunity(Long userId, Long opportunityId) {
        savedOpportunityRepository.deleteByUserIdAndOpportunityId(userId, opportunityId);
    }

    public List<OpportunityDto> getSavedOpportunities(Long userId) {
        return savedOpportunityRepository.findByUserIdOrderByCreatedAtDesc(userId)
                .stream()
                .map(s -> opportunityService.mapToDto(s.getOpportunity(), userId))
                .collect(Collectors.toList());
    }

    public boolean isOpportunitySaved(Long userId, Long opportunityId) {
        return savedOpportunityRepository.existsByUserIdAndOpportunityId(userId, opportunityId);
    }
}
