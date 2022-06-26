export default class TimeUtil {

    public static timestampToDateString(timestamp: number): string {
        return new Date(timestamp).toISOString().split('T')[0];
    }
}
