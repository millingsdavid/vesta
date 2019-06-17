function myFunction() {
    var symbol = document.getElementById("symbol").value;  
            localStorage.setItem("symbol_session", symbol);
            console.log(localStorage.getItem("symbol_session"));
}
    $(document).ready(function(){
        var API_KEY = 'DK77QBBTBPAHB43CYOUR_API_KEY';
        var symbol = localStorage.getItem("symbol_session");
            console.log("Submit Symbol: " + symbol)
        $.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + symbol + '&apikey=' + API_KEY, function(res) {
            console.log(res);
           
            var high =  res['Global Quote']['03. high'];
            var low =  res['Global Quote']['04. low'];
            var close =  res['Global Quote']['08. previous close'];
            var pivotPoint =  (parseFloat(high) + parseFloat(low) + parseFloat(close)) / 3;
            var resistance = (2 * pivotPoint) - parseFloat(low);
            var support = (2 * pivotPoint) - parseFloat(high);
            console.log("Symbol: " + symbol);
            console.log("High: " + high);
            console.log("Low: " + low);
            console.log("Close: " + close);
            console.log("Pivot Point: " + pivotPoint.toFixed(2));
            console.log("Resistance: " + resistance.toFixed(2));
            console.log("Support: " + support.toFixed(2));
            $('#symbol_title').html("<span>" + symbol + "</span>")
            $('#high').html("<span>" + parseFloat(high).toFixed(2) + "</span>")
            $('#low').html("<span>" + parseFloat(low).toFixed(2) + "</span>")
            $('#close').html("<span>" + parseFloat(close).toFixed(2) + "</span>")
            $('#resistance').html("<span>" + parseFloat(resistance).toFixed(2) + "</span>")
            $('#support').html("<span>" + parseFloat(support).toFixed(2) + "</span>")
        }, "json");
    })