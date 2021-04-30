package com.masterson.api.model.binance;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class ExchangeInfo {
    private String timezone;
    private long serverTime;
    private List<?> rateLimits;
    private List<?> exchangeFilters;
    private List<Symbol> symbols;
}
