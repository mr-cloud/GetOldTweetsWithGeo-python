var colors =
    [ "#0000FF",
      "#0066FF",
      "#3399FF",
      "#66CCFF",
      "#CCFFFF",
      "#CCFFCC",
      "#FFFFCC",
      "#FFFF99",
      "#FFFF66",
      "#FFFF33",
      "#FFFF00"];


var mapData = {
    "c1001": colors[0],
    "c1003": colors[3],
    "c6071": colors[6],
    "c1131": colors[9],
    "c72153": colors[10],
    "c32007": "red"
};

var map = new Datamap({
    element: document.getElementById('container'),

    scope: 'counties',
    setProjection: function(element, options) {
        var projection, path;
        projection = d3.geo.albersUsa()
            .scale(element.offsetWidth)
            .translate([element.offsetWidth / 2, element.offsetHeight / 2]);

        path = d3.geo.path()
            .projection( projection );

        return {path: path, projection: projection};
    },
    fills: {
            HIGH: '#afafaf',
            LOW: 'red',
            MEDIUM: 'blue',
            UNKNOWN: 'rgb(0,0,0)',
            defaultFill: 'green'
    },

    data: {
            'c6071': {
                fillKey: 'LOW'
            },
            'c32007': {
                fillKey: 'MEDIUM'
            }
/*            'c6071': '#123456',
            'c32007': '#afafaf'*/
         },

    geographyConfig: {
        dataUrl: '/static/us.json',
        popupTemplate: function(geo, data) {

//          var lineOfTweets = "<p>" + hashSentence[geo.id] + "</p>";
          var lineOfTweets = "#TimesSquare";
          console.log(geo.id + ':' + lineOfTweets)

            return ['<div class="hoverinfo"><strong>',
                    'Top tweets in ', countyLookup[geo.id],  lineOfTweets,
                    '</strong></div>'].join('');
        }
    }
});

//map.updateChoropleth(mapData);
map.updateChoropleth({c32007: {fillKey: 'LOW'}}, {reset: true})
// doesnot work!
//map.updateChoropleth({'c32007': 'red'}, {reset: true})