package com.jansetu.repository;

import com.jansetu.entity.Opportunity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface OpportunityRepository extends JpaRepository<Opportunity, Long> {

    Optional<Opportunity> findBySlug(String slug);

    List<Opportunity> findByStatus(String status);

    @Query("SELECT o FROM Opportunity o WHERE o.status = 'ACTIVE' " +
           "AND (:category IS NULL OR LOWER(o.category) = :category) " +
           "AND (:type IS NULL OR LOWER(o.type) = :type) " +
           "AND (:govtLevel IS NULL OR LOWER(o.governmentLevel) = :govtLevel) " +
           "AND (:state IS NULL OR o.state IS NULL OR LOWER(o.state) = :state OR LOWER(o.state) = 'all india') " +
           "AND (:search IS NULL OR LOWER(o.name) LIKE :search " +
           "     OR (o.shortDescription IS NOT NULL AND LOWER(o.shortDescription) LIKE :search) " +
           "     OR (o.tags IS NOT NULL AND LOWER(o.tags) LIKE :search))")
    Page<Opportunity> findWithFilters(
            @Param("category") String category,
            @Param("type") String type,
            @Param("govtLevel") String govtLevel,
            @Param("state") String state,
            @Param("search") String search,
            Pageable pageable
    );

    @Query("SELECT DISTINCT o.category FROM Opportunity o WHERE o.category IS NOT NULL AND o.status = 'ACTIVE'")
    List<String> findDistinctCategories();

    @Query("SELECT DISTINCT o.type FROM Opportunity o WHERE o.type IS NOT NULL AND o.status = 'ACTIVE'")
    List<String> findDistinctTypes();

    @Query("SELECT DISTINCT o.state FROM Opportunity o WHERE o.state IS NOT NULL AND o.status = 'ACTIVE'")
    List<String> findDistinctStates();

    @Query("SELECT COUNT(o) FROM Opportunity o WHERE o.status = 'ACTIVE'")
    long countActive();
}
