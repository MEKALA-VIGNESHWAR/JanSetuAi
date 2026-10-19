package com.jansetu.controller;

import com.jansetu.dto.OpportunityDto;
import com.jansetu.service.OpportunityService;
import com.jansetu.util.SecurityUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/opportunities")
public class OpportunityController {

    private final OpportunityService opportunityService;

    public OpportunityController(OpportunityService opportunityService) {
        this.opportunityService = opportunityService;
    }

    @GetMapping
    public ResponseEntity<Page<OpportunityDto>> getOpportunities(
            @RequestParam(required = false) String category,
            @RequestParam(required = false) String type,
            @RequestParam(required = false) String govtLevel,
            @RequestParam(required = false) String state,
            @RequestParam(required = false) String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "12") int size,
            @RequestParam(defaultValue = "id,desc") String sort) {

        String[] sortParams = sort.split(",");
        String sortField = sortParams[0];
        Sort.Direction direction = sortParams.length > 1 && sortParams[1].equalsIgnoreCase("asc")
                ? Sort.Direction.ASC
                : Sort.Direction.DESC;

        Pageable pageable = PageRequest.of(page, size, Sort.by(direction, sortField));
        Long currentUserId = SecurityUtils.getCurrentUserId();

        return ResponseEntity.ok(opportunityService.getOpportunities(
                category, type, govtLevel, state, search, pageable, currentUserId
        ));
    }

    @GetMapping("/{id}")
    public ResponseEntity<OpportunityDto> getOpportunityById(@PathVariable Long id) {
        Long currentUserId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(opportunityService.getOpportunityById(id, currentUserId));
    }

    @GetMapping("/slug/{slug}")
    public ResponseEntity<OpportunityDto> getOpportunityBySlug(@PathVariable String slug) {
        Long currentUserId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(opportunityService.getOpportunityBySlug(slug, currentUserId));
    }

    @GetMapping("/categories")
    public ResponseEntity<List<String>> getCategories() {
        return ResponseEntity.ok(opportunityService.getCategories());
    }

    @GetMapping("/types")
    public ResponseEntity<List<String>> getTypes() {
        return ResponseEntity.ok(opportunityService.getTypes());
    }

    @GetMapping("/states")
    public ResponseEntity<List<String>> getStates() {
        return ResponseEntity.ok(opportunityService.getStates());
    }

    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getStats() {
        return ResponseEntity.ok(opportunityService.getStats());
    }
}
