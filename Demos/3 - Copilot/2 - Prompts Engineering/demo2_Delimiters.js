// Create a function that returns the days between two dates
function daysBetween(date1, date2) {
    const oneDay = 24 * 60 * 60 * 1000;
    if (!(date1 instanceof Date) || !(date2 instanceof Date)) {
        throw new Error("Both arguments must be valid Date objects.");
    }
    const diffDays = Math.abs((date2 - date1) / oneDay);
    return Math.round(diffDays);
}
