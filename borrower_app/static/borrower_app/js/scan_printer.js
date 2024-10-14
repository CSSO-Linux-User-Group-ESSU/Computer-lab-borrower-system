function ScanPrinter(){
            fetch('/scan_printer/')
            .then(response => response.text())
            .then(data => alert(data))
            .catch(error => console.error("Error:", error))
        }