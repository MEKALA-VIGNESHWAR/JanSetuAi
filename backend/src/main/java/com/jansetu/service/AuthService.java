package com.jansetu.service;

import com.jansetu.dto.AuthDto;
import com.jansetu.entity.CitizenProfile;
import com.jansetu.entity.User;
import com.jansetu.repository.CitizenProfileRepository;
import com.jansetu.repository.UserRepository;
import com.jansetu.security.JwtTokenProvider;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final CitizenProfileRepository citizenProfileRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtTokenProvider tokenProvider;

    public AuthService(
            UserRepository userRepository,
            CitizenProfileRepository citizenProfileRepository,
            PasswordEncoder passwordEncoder,
            AuthenticationManager authenticationManager,
            JwtTokenProvider tokenProvider) {
        this.userRepository = userRepository;
        this.citizenProfileRepository = citizenProfileRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.tokenProvider = tokenProvider;
    }

    @Transactional
    public AuthDto.AuthResponse register(AuthDto.RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new IllegalArgumentException("Email already registered: " + request.getEmail());
        }

        String role = (request.getRole() != null && request.getRole().equalsIgnoreCase("ADMIN")) ? "ADMIN" : "USER";

        User user = User.builder()
                .email(request.getEmail().toLowerCase().trim())
                .passwordHash(passwordEncoder.encode(request.getPassword()))
                .role(role)
                .isActive(true)
                .build();

        User savedUser = userRepository.save(user);

        // Initialize empty profile
        CitizenProfile profile = CitizenProfile.builder()
                .user(savedUser)
                .fullName(request.getFullName())
                .profileCompletion(request.getFullName() != null && !request.getFullName().isBlank() ? 10 : 0)
                .onboardingStep(1)
                .build();
        citizenProfileRepository.save(profile);

        String token = tokenProvider.generateTokenFromUserId(savedUser.getId(), savedUser.getEmail());

        return AuthDto.AuthResponse.builder()
                .token(token)
                .tokenType("Bearer")
                .userId(savedUser.getId())
                .email(savedUser.getEmail())
                .role(savedUser.getRole())
                .fullName(profile.getFullName())
                .profileCompletion(profile.getProfileCompletion())
                .build();
    }

    public AuthDto.AuthResponse login(AuthDto.LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getEmail().toLowerCase().trim(),
                        request.getPassword()
                )
        );

        User user = userRepository.findByEmail(request.getEmail().toLowerCase().trim())
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        CitizenProfile profile = citizenProfileRepository.findByUserId(user.getId()).orElse(null);

        String token = tokenProvider.generateToken(authentication);

        return AuthDto.AuthResponse.builder()
                .token(token)
                .tokenType("Bearer")
                .userId(user.getId())
                .email(user.getEmail())
                .role(user.getRole())
                .fullName(profile != null ? profile.getFullName() : null)
                .profileCompletion(profile != null ? profile.getProfileCompletion() : 0)
                .build();
    }

    public AuthDto.UserDto getCurrentUser(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found with id: " + userId));
        return AuthDto.UserDto.builder()
                .id(user.getId())
                .email(user.getEmail())
                .role(user.getRole())
                .isActive(user.getIsActive())
                .build();
    }
}
