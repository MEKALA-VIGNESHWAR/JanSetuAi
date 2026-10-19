package com.jansetu.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class AuthDto {

    public static class RegisterRequest {
        @NotBlank(message = "Email is required")
        @Email(message = "Valid email is required")
        private String email;

        @NotBlank(message = "Password is required")
        @Size(min = 6, message = "Password must be at least 6 characters")
        private String password;

        private String fullName;
        private String role;

        public RegisterRequest() {}

        public RegisterRequest(String email, String password, String fullName, String role) {
            this.email = email;
            this.password = password;
            this.fullName = fullName;
            this.role = role;
        }

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
        public String getFullName() { return fullName; }
        public void setFullName(String fullName) { this.fullName = fullName; }
        public String getRole() { return role; }
        public void setRole(String role) { this.role = role; }
    }

    public static class LoginRequest {
        @NotBlank(message = "Email is required")
        @Email(message = "Valid email is required")
        private String email;

        @NotBlank(message = "Password is required")
        private String password;

        public LoginRequest() {}

        public LoginRequest(String email, String password) {
            this.email = email;
            this.password = password;
        }

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
    }

    public static class AuthResponse {
        private String token;
        private String tokenType = "Bearer";
        private Long userId;
        private String email;
        private String role;
        private Integer profileCompletion;
        private String fullName;

        public AuthResponse() {}

        public static Builder builder() { return new Builder(); }

        public static class Builder {
            private final AuthResponse res = new AuthResponse();
            public Builder token(String token) { res.token = token; return this; }
            public Builder tokenType(String tokenType) { res.tokenType = tokenType; return this; }
            public Builder userId(Long userId) { res.userId = userId; return this; }
            public Builder email(String email) { res.email = email; return this; }
            public Builder role(String role) { res.role = role; return this; }
            public Builder profileCompletion(Integer comp) { res.profileCompletion = comp; return this; }
            public Builder fullName(String fullName) { res.fullName = fullName; return this; }
            public AuthResponse build() { return res; }
        }

        public String getToken() { return token; }
        public void setToken(String token) { this.token = token; }
        public String getTokenType() { return tokenType; }
        public void setTokenType(String tokenType) { this.tokenType = tokenType; }
        public Long getUserId() { return userId; }
        public void setUserId(Long userId) { this.userId = userId; }
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        public String getRole() { return role; }
        public void setRole(String role) { this.role = role; }
        public Integer getProfileCompletion() { return profileCompletion; }
        public void setProfileCompletion(Integer profileCompletion) { this.profileCompletion = profileCompletion; }
        public String getFullName() { return fullName; }
        public void setFullName(String fullName) { this.fullName = fullName; }
    }

    public static class UserDto {
        private Long id;
        private String email;
        private String role;
        private Boolean isActive;

        public UserDto() {}

        public static Builder builder() { return new Builder(); }

        public static class Builder {
            private final UserDto u = new UserDto();
            public Builder id(Long id) { u.id = id; return this; }
            public Builder email(String email) { u.email = email; return this; }
            public Builder role(String role) { u.role = role; return this; }
            public Builder isActive(Boolean isActive) { u.isActive = isActive; return this; }
            public UserDto build() { return u; }
        }

        public Long getId() { return id; }
        public void setId(Long id) { this.id = id; }
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        public String getRole() { return role; }
        public void setRole(String role) { this.role = role; }
        public Boolean getIsActive() { return isActive; }
        public void setIsActive(Boolean isActive) { this.isActive = isActive; }
    }
}
