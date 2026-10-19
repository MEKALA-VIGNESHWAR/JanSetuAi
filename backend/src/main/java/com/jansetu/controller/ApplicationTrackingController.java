package com.jansetu.controller;

import com.jansetu.dto.ApplicationTrackingDto;
import com.jansetu.service.ApplicationTrackingService;
import com.jansetu.util.SecurityUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/tracking")
public class ApplicationTrackingController {

    private final ApplicationTrackingService trackingService;

    public ApplicationTrackingController(ApplicationTrackingService trackingService) {
        this.trackingService = trackingService;
    }

    @GetMapping
    public ResponseEntity<List<ApplicationTrackingDto>> getUserTrackings() {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }
        return ResponseEntity.ok(trackingService.getUserTrackings(userId));
    }

    @PostMapping
    public ResponseEntity<ApplicationTrackingDto> trackOpportunity(@RequestBody ApplicationTrackingDto dto) {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }
        return ResponseEntity.ok(trackingService.trackOpportunity(
                userId, dto.getOpportunityId(), dto.getStatus(), dto.getNotes(), dto.getAppliedDate()
        ));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, String>> deleteTracking(@PathVariable Long id) {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }
        trackingService.deleteTracking(userId, id);
        return ResponseEntity.ok(Map.of("message", "Tracking removed successfully"));
    }
}
