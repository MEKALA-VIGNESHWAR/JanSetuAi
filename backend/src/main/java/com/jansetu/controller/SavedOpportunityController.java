package com.jansetu.controller;

import com.jansetu.dto.OpportunityDto;
import com.jansetu.service.SavedOpportunityService;
import com.jansetu.util.SecurityUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/saved")
public class SavedOpportunityController {

    private final SavedOpportunityService savedOpportunityService;

    public SavedOpportunityController(SavedOpportunityService savedOpportunityService) {
        this.savedOpportunityService = savedOpportunityService;
    }

    @GetMapping
    public ResponseEntity<List<OpportunityDto>> getSavedOpportunities() {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }
        return ResponseEntity.ok(savedOpportunityService.getSavedOpportunities(userId));
    }

    @PostMapping("/{opportunityId}")
    public ResponseEntity<Map<String, String>> saveOpportunity(@PathVariable Long opportunityId) {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }
        savedOpportunityService.saveOpportunity(userId, opportunityId);
        return ResponseEntity.ok(Map.of("message", "Opportunity saved successfully"));
    }

    @DeleteMapping("/{opportunityId}")
    public ResponseEntity<Map<String, String>> unsaveOpportunity(@PathVariable Long opportunityId) {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }
        savedOpportunityService.unsaveOpportunity(userId, opportunityId);
        return ResponseEntity.ok(Map.of("message", "Opportunity unsaved successfully"));
    }
}
