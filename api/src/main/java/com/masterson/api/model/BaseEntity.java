package com.masterson.api.model;

import lombok.Getter;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;

import javax.persistence.Column;
import javax.persistence.MappedSuperclass;
import java.io.Serializable;
import java.time.ZonedDateTime;

@MappedSuperclass
@Getter
public class BaseEntity implements Serializable {

    @CreatedDate
    @Column(name = "CREATED_DT")
    private ZonedDateTime createdDateTime;

    @LastModifiedDate
    @Column(name = "LAST_UPDATED_DT")
    private ZonedDateTime lastUpdatedDateTime;
}
