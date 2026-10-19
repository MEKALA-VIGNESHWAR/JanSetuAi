package com.jansetu.controller;

import com.jansetu.dto.FeedbackDto;
import com.jansetu.service.FeedbackService;
import com.jansetu.util.SecurityUtils;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/feedback")
public class FeedbackController {

    private final FeedbackService feedbackService;

    public FeedbackController(FeedbackService feedbackService) {
        this.feedbackService = feedbackService;
    }

    @PostMapping("/submit")
    public ResponseEntity<FeedbackDto> submitFeedback(@Valid @RequestBody FeedbackDto dto) {
        Long userId = SecurityUtils.getCurrentUserId(); // Can be null if not logged in
        return ResponseEntity.ok(feedbackService.submitFeedback(userId, dto));
    }

    @GetMapping("/list")
    public ResponseEntity<List<FeedbackDto>> getAllFeedback() {
        return ResponseEntity.ok(feedbackService.getAllFeedback());
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<FeedbackDto> updateFeedbackStatus(
            @PathVariable Long id,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String adminNotes) {
        return ResponseEntity.ok(feedbackService.updateFeedbackStatus(id, status, adminNotes));
    }
}
