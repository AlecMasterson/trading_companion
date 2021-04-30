package com.masterson.api.model;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Builder
@Getter
@Setter
public class Candle {
    private float close;
    private String closeTime;
    private float high;
    private Interval interval;
    private float low;
    private float open;
    private String openTime;
    private Source source;
    private String ticker;
}
