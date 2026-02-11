function daysBetween(date1, date2) {
    const oneDay = 24 * 60 * 60 * 1000;
    if (!date1 || !date2 || !(date1 instanceof Date) || !(date2 instanceof Date) || isNaN(date1.getTime()) || isNaN(date2.getTime())) {
        throw new Error("Both arguments must be valid Date objects and cannot be null, undefined, or invalid.");
    }
    const diffDays = Math.abs((date2.getTime() - date1.getTime()) / oneDay);
    return Math.round(diffDays);
}

// Example usage:
try {
    const date1 = new Date('2023-01-01');
    const date2 = new Date('2023-01-10');
    console.log(daysBetween(date1, date2)); // Output: 9
} catch (error) {
    console.error(error.message);
}
