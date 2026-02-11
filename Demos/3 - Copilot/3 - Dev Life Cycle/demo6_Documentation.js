


/**
 * Calculates the number of days between two dates.
 *
 * @param {Date} date1 - The start date.
 * @param {Date} date2 - The end date.
 * @returns {number} The number of days between the two dates. A positive value indicates that date2 is after date1, 
 * while a negative value indicates that date2 is before date1.
 */


function daysBetweenDates(date1, date2) {
    const diff = date2.getTime() - date1.getTime();
    return diff / (1000 * 60 * 60 * 24);
}




daysBetweenDates(new Date('2023-01-01'), new Date('2023-01-10')); // Returns 9