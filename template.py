html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<title>Dustball SEA2SAN</title>
</head>
<body>
<div id="container">
    <div id="map" style="width:100%; height:1000px"></div>
</div>

<script>
    function initMap() {
        const directionsService = new google.maps.DirectionsService();
        const directionsRenderer = new google.maps.DirectionsRenderer();
        const map = new google.maps.Map(document.getElementById("map"));

        const origin = "{ORIGIN}";
        const destination = "{DESTINATION}";
        const wp_raw = {WAYPOINTS};
        var waypoints = [];
        for (const wp of wp_raw) {
            waypoints.push({
                location: {placeId: wp},
                stopover: false,
            });
        };

        directionsRenderer.setMap(map);
        directionsService.route({
            "origin": {placeId: origin},
            "destination": {placeId: destination},
            "waypoints": waypoints,
            travelMode: google.maps.TravelMode.DRIVING,
        })
        .then((response) => {
            directionsRenderer.setDirections(response);
        })
    }
</script>

<script src="https://maps.googleapis.com/maps/api/js?key={API_KEY}&callback=initMap">
</script>

</body>
</html>
"""
