package com.jansetu.controller;

import com.jansetu.dto.CitizenProfileDto;
import com.jansetu.dto.MatchedOpportunityDto;
import com.jansetu.entity.CitizenProfile;
import com.jansetu.service.CitizenProfileService;
import com.jansetu.service.EligibilityEngineService;
import com.jansetu.util.SecurityUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/match")
public class MatchingController {

    private final EligibilityEngineService eligibilityEngineService;
    private final CitizenProfileService profileService;

    public MatchingController(EligibilityEngineService eligibilityEngineService, CitizenProfileService profileService) {
        this.eligibilityEngineService = eligibilityEngineService;
        this.profileService = profileService;
    }

    @GetMapping("/schemes")
    public ResponseEntity<List<MatchedOpportunityDto>> matchSchemesForCurrentUser() {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return ResponseEntity.status(401).build();
        }

        CitizenProfile profile = profileService.getProfileEntity(userId);
        List<MatchedOpportunityDto> results = eligibilityEngineService.matchOpportunitiesForCitizen(profile);
        return ResponseEntity.ok(results);
    }

    @PostMapping("/preview")
    public ResponseEntity<List<MatchedOpportunityDto>> matchSchemesPreview(@RequestBody CitizenProfileDto profileDto) {
        // Construct temporary in-memory CitizenProfile entity for guest evaluation
        CitizenProfile tempProfile = CitizenProfile.builder()
                .fullName(profileDto.getFullName())
                .age(profileDto.getAge())
                .gender(profileDto.getGender())
                .state(profileDto.getState())
                .district(profileDto.getDistrict())
                .areaType(profileDto.getAreaType())
                .educationLevel(profileDto.getEducationLevel())
                .courseStream(profileDto.getCourseStream())
                .isStudent(profileDto.getIsStudent())
                .collegeType(profileDto.getCollegeType())
                .occupation(profileDto.getOccupation())
                .annualIncome(profileDto.getAnnualIncome())
                .incomeCategory(profileDto.getIncomeCategory())
                .employmentStatus(profileDto.getEmploymentStatus())
                .socialCategory(profileDto.getSocialCategory())
                .isPwd(profileDto.getIsPwd())
                .disabilityType(profileDto.getDisabilityType())
                .maritalStatus(profileDto.getMaritalStatus())
                .isWidow(profileDto.getIsWidow())
                .isSingleWoman(profileDto.getIsSingleWoman())
                .isFarmer(profileDto.getIsFarmer())
                .hasLivestock(profileDto.getHasLivestock())
                .ownsLand(profileDto.getOwnsLand())
                .landHoldingAcres(profileDto.getLandHoldingAcres())
                .cropType(profileDto.getCropType())
                .hasBusiness(profileDto.getHasBusiness())
                .businessType(profileDto.getBusinessType())
                .build();

        List<MatchedOpportunityDto> results = eligibilityEngineService.matchOpportunitiesForCitizen(tempProfile);
        return ResponseEntity.ok(results);
    }
}
