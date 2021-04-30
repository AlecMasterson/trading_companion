package com.masterson.api.model.coinbase;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Product {
    private String id;
    private String displayName;
    private String baseCurrency;
    private String quoteCurrency;
    private String baseIncrement;
    private String quoteIncrement;
    private String baseMinSize;
    private String baseMaxSize;
    private String minMarketFunds;
    private String maxMarketFunds;
    private String status;
    private String statusMessage;
    private boolean cancelOnly;
    private boolean limitOnly;
    private boolean postOnly;
    private boolean tradingDisabled;
    private boolean fxStablecoin;
}
