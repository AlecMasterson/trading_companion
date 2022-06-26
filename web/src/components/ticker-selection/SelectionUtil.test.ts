import SelectionUtil from './SelectionUtil';
import {iTickerSummary} from '../../types/iTickerSummary';

describe('filterTickers', () => {

    const tickers: iTickerSummary[] = [
        {currentPrice: 0, name: 'name1', source: 'source1'},
        {currentPrice: 0, name: 'otherNAME1', source: 'source1'},
        {currentPrice: 0, name: 'other-also', source: 'first-beach'},
        {currentPrice: 0, name: 'name2', source: 'second-BEAch'}
    ];

    it('should return an empty array if an empty array is given', () => {
        expect(SelectionUtil.filterTickers([], '')).toEqual([]);
    });

    it('should return the original array if the filter value is empty', () => {
        expect(SelectionUtil.filterTickers(tickers, '')).toEqual(tickers);
    });

    it('should keep based on partial/full match with the source', () => {
        expect(SelectionUtil.filterTickers(tickers, 'first-')).toEqual([tickers[2]]);
        expect(SelectionUtil.filterTickers(tickers, 'first-beach')).toEqual([tickers[2]]);
    });

    it('should keep based on case-insensitive match with the source', () => {
        expect(SelectionUtil.filterTickers(tickers, 'bea')).toEqual(tickers.slice(2));
        expect(SelectionUtil.filterTickers(tickers, 'BEA')).toEqual(tickers.slice(2));
    });

    it('should keep based on partial/full match with the name', () => {
        expect(SelectionUtil.filterTickers(tickers, 'oth')).toEqual(tickers.slice(1, 3));
        expect(SelectionUtil.filterTickers(tickers, 'other-also')).toEqual([tickers[2]]);
    });

    it('should keep based on case-insensitive match with the name', () => {
        expect(SelectionUtil.filterTickers(tickers, 'name1')).toEqual(tickers.slice(0, 2));
        expect(SelectionUtil.filterTickers(tickers, 'NAME1')).toEqual(tickers.slice(0, 2));
    });
});

describe('isTickerEqual', () => {
    it('should return true if both are null', () => {
        expect(SelectionUtil.isTickerEqual(null, null)).toBeTruthy();
    });

    it('should return false if only one is null', () => {
        const summary: iTickerSummary = {currentPrice: 0, name: 'name1', source: 'source1'};

        expect(SelectionUtil.isTickerEqual(summary, null)).toBeFalsy();
        expect(SelectionUtil.isTickerEqual(null, summary)).toBeFalsy();
    });

    it('should return false if the source does not match', () => {
        const summary1: iTickerSummary = {currentPrice: 0, name: 'name1', source: 'source1'};
        const summary2: iTickerSummary = {currentPrice: 0, name: 'name1', source: 'source2'};

        expect(SelectionUtil.isTickerEqual(summary1, summary2)).toBeFalsy();
    });

    it('should return false if the name does not match', () => {
        const summary1: iTickerSummary = {currentPrice: 0, name: 'name1', source: 'source1'};
        const summary2: iTickerSummary = {currentPrice: 0, name: 'name2', source: 'source1'};

        expect(SelectionUtil.isTickerEqual(summary1, summary2)).toBeFalsy();
    });

    it('should return false if both the source and name does not match', () => {
        const summary1: iTickerSummary = {currentPrice: 0, name: 'name1', source: 'source1'};
        const summary2: iTickerSummary = {currentPrice: 0, name: 'name2', source: 'source2'};

        expect(SelectionUtil.isTickerEqual(summary1, summary2)).toBeFalsy();
    });

    it('should return true if both the source and name match', () => {
        const summary: iTickerSummary = {currentPrice: 0, name: 'name1', source: 'source1'};

        expect(SelectionUtil.isTickerEqual(summary, summary)).toBeTruthy();
    });
});
