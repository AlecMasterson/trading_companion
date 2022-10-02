import NumberUtil from './NumberUtil';

describe('formatDollar', () => {
    it('should format zero to "$0.00"', () => {
        expect(NumberUtil.formatDollar(0)).toEqual('$0.00');
    });

    it('should round the decimal value', () => {
        expect(NumberUtil.formatDollar(1.0044)).toEqual('$1.00');
        expect(NumberUtil.formatDollar(1.0045)).toEqual('$1.01');
    });

    it('should add commas for larger numbers', () => {
        expect(NumberUtil.formatDollar(5335.215)).toEqual('$5,335.22');
        expect(NumberUtil.formatDollar(8922351.899)).toEqual('$8,922,351.90');
    });
});
