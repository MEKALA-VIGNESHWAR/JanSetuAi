package com.jansetu.controller;

import com.jansetu.dto.CitizenProfileDto;
import com.jansetu.service.CitizenProfileService;
import com.jansetu.util.SecurityUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/profile")
public class ProfileController {

    private final CitizenProfileService profileService;

    public ProfileController(CitizenProfileService profileService) {
        this.profileService = profileService;
    }

    @GetMapping
    public ResponseEntity<CitizenProfileDto> getProfile() {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }
        return ResponseEntity.ok(profileService.getProfile(userId));
    }

    @PutMapping
    public ResponseEntity<CitizenProfileDto> updateProfile(@RequestBody CitizenProfileDto profileDto) {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }
        return ResponseEntity.ok(profileService.updateProfile(userId, profileDto));
    }
}
