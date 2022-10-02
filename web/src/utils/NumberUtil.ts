const Formatter_USD = new Intl.NumberFormat('en-US', {
    currency: 'USD',
    style: 'currency'
});

export default class NumberUtil {

    public static formatDollar(value: number): string {
        return Formatter_USD.format(value);
    }
}
