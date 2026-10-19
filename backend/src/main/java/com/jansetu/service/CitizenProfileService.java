package com.jansetu.service;

import com.jansetu.dto.CitizenProfileDto;
import com.jansetu.entity.CitizenProfile;
import com.jansetu.entity.User;
import com.jansetu.repository.CitizenProfileRepository;
import com.jansetu.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CitizenProfileService {

    private final CitizenProfileRepository profileRepository;
    private final UserRepository userRepository;

    public CitizenProfileService(CitizenProfileRepository profileRepository, UserRepository userRepository) {
        this.profileRepository = profileRepository;
        this.userRepository = userRepository;
    }

    public CitizenProfileDto getProfile(Long userId) {
        CitizenProfile profile = profileRepository.findByUserId(userId)
                .orElseGet(() -> createDefaultProfile(userId));
        return toDto(profile);
    }

    @Transactional
    public CitizenProfileDto updateProfile(Long userId, CitizenProfileDto dto) {
        CitizenProfile profile = profileRepository.findByUserId(userId)
                .orElseGet(() -> createDefaultProfile(userId));

        // Update fields if provided in dto
        if (dto.getFullName() != null) profile.setFullName(dto.getFullName());
        if (dto.getAge() != null) profile.setAge(dto.getAge());
        if (dto.getGender() != null) profile.setGender(dto.getGender());
        if (dto.getState() != null) profile.setState(dto.getState());
        if (dto.getDistrict() != null) profile.setDistrict(dto.getDistrict());
        if (dto.getAreaType() != null) profile.setAreaType(dto.getAreaType());

        if (dto.getEducationLevel() != null) profile.setEducationLevel(dto.getEducationLevel());
        if (dto.getCourseStream() != null) profile.setCourseStream(dto.getCourseStream());
        if (dto.getIsStudent() != null) profile.setIsStudent(dto.getIsStudent());
        if (dto.getCollegeType() != null) profile.setCollegeType(dto.getCollegeType());

        if (dto.getOccupation() != null) profile.setOccupation(dto.getOccupation());
        if (dto.getAnnualIncome() != null) profile.setAnnualIncome(dto.getAnnualIncome());
        if (dto.getIncomeCategory() != null) profile.setIncomeCategory(dto.getIncomeCategory());
        if (dto.getEmploymentStatus() != null) profile.setEmploymentStatus(dto.getEmploymentStatus());

        if (dto.getSocialCategory() != null) profile.setSocialCategory(dto.getSocialCategory());
        if (dto.getIsPwd() != null) profile.setIsPwd(dto.getIsPwd());
        if (dto.getDisabilityType() != null) profile.setDisabilityType(dto.getDisabilityType());

        if (dto.getMaritalStatus() != null) profile.setMaritalStatus(dto.getMaritalStatus());
        if (dto.getIsWidow() != null) profile.setIsWidow(dto.getIsWidow());
        if (dto.getIsSingleWoman() != null) profile.setIsSingleWoman(dto.getIsSingleWoman());

        if (dto.getIsFarmer() != null) profile.setIsFarmer(dto.getIsFarmer());
        if (dto.getHasLivestock() != null) profile.setHasLivestock(dto.getHasLivestock());
        if (dto.getOwnsLand() != null) profile.setOwnsLand(dto.getOwnsLand());
        if (dto.getLandHoldingAcres() != null) profile.setLandHoldingAcres(dto.getLandHoldingAcres());
        if (dto.getCropType() != null) profile.setCropType(dto.getCropType());

        if (dto.getHasBusiness() != null) profile.setHasBusiness(dto.getHasBusiness());
        if (dto.getBusinessType() != null) profile.setBusinessType(dto.getBusinessType());

        if (dto.getOnboardingStep() != null) profile.setOnboardingStep(dto.getOnboardingStep());
        if (dto.getPrimaryRole() != null) profile.setPrimaryRole(dto.getPrimaryRole());

        // Recalculate profile completion percentage
        profile.setProfileCompletion(calculateCompletion(profile));

        CitizenProfile saved = profileRepository.save(profile);
        return toDto(saved);
    }

    public CitizenProfile getProfileEntity(Long userId) {
        return profileRepository.findByUserId(userId)
                .orElseGet(() -> createDefaultProfile(userId));
    }

    private CitizenProfile createDefaultProfile(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found: " + userId));
        CitizenProfile newProfile = CitizenProfile.builder()
                .user(user)
                .profileCompletion(0)
                .onboardingStep(1)
                .build();
        return profileRepository.save(newProfile);
    }

    public int calculateCompletion(CitizenProfile p) {
        int total = 10;
        int completed = 0;

        if (p.getFullName() != null && !p.getFullName().isBlank()) completed++;
        if (p.getAge() != null && p.getAge() > 0) completed++;
        if (p.getGender() != null && !p.getGender().isBlank()) completed++;
        if (p.getState() != null && !p.getState().isBlank()) completed++;
        if (p.getDistrict() != null && !p.getDistrict().isBlank()) completed++;
        if (p.getEducationLevel() != null && !p.getEducationLevel().isBlank()) completed++;
        if (p.getOccupation() != null && !p.getOccupation().isBlank()) completed++;
        if (p.getAnnualIncome() != null) completed++;
        if (p.getSocialCategory() != null && !p.getSocialCategory().isBlank()) completed++;
        if (p.getAreaType() != null && !p.getAreaType().isBlank()) completed++;

        return (int) Math.round(((double) completed / total) * 100);
    }

    private CitizenProfileDto toDto(CitizenProfile p) {
        return CitizenProfileDto.builder()
                .id(p.getId())
                .userId(p.getUser().getId())
                .fullName(p.getFullName())
                .age(p.getAge())
                .gender(p.getGender())
                .state(p.getState())
                .district(p.getDistrict())
                .areaType(p.getAreaType())
                .educationLevel(p.getEducationLevel())
                .courseStream(p.getCourseStream())
                .isStudent(p.getIsStudent())
                .collegeType(p.getCollegeType())
                .occupation(p.getOccupation())
                .annualIncome(p.getAnnualIncome())
                .incomeCategory(p.getIncomeCategory())
                .employmentStatus(p.getEmploymentStatus())
                .socialCategory(p.getSocialCategory())
                .isPwd(p.getIsPwd())
                .disabilityType(p.getDisabilityType())
                .maritalStatus(p.getMaritalStatus())
                .isWidow(p.getIsWidow())
                .isSingleWoman(p.getIsSingleWoman())
                .isFarmer(p.getIsFarmer())
                .hasLivestock(p.getHasLivestock())
                .ownsLand(p.getOwnsLand())
                .landHoldingAcres(p.getLandHoldingAcres())
                .cropType(p.getCropType())
                .hasBusiness(p.getHasBusiness())
                .businessType(p.getBusinessType())
                .profileCompletion(p.getProfileCompletion())
                .onboardingStep(p.getOnboardingStep())
                .primaryRole(p.getPrimaryRole())
                .updatedAt(p.getUpdatedAt())
                .build();
    }
}
