// Cretae a function that creaates a proper XML from the following JSONs:
// [{name : 'Ron', age : 20}, {name : 'John', age : 30}]

function jsonToXml(jsonArray) {
    let xml = '<root>\n'
    jsonArray.forEach(item => {
        xml += '  <person>\n'
        for (let key in item) {
            xml += `    <${key}>${item[key]}</${key}>\n`
        }
        xml += '  </person>\n'
    });
    xml += '</root>';
    return xml;
}