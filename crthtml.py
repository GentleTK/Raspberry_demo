#coding=UTF-8
GEN_HTML = "MarkPoint.html"
f = open(GEN_HTML,"w")
message = """
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
        body, html{width: 100%;height: 100%;margin:0;font-family:"微软雅黑";}
	#allmap{height:100%;width:100%;}
    </style>
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=wgYlWnYQSZ5fN3RdCxYoIF8jT7y1jRLb"></script>
    <title>Map Marking</title>
</head>
<body>
    <p id="allmap"></p>
<script type="text/javascript">
    // 百度地图API功能
    var map = new BMap.Map("allmap");
    map.centerAndZoom(new BMap.Point(116.331398,39.897445),11);
    map.enableScrollWheelZoom(true);
	 // 用经纬度设置地图中心点
    function theLocation(){
        map.clearOverlays();
	//GPS to BD Coordinate
	//var new_point = new BMap.Point(113.5359, 26.7725);
	var new_point = new BMap.Point(112.9378, 27.8533);
	//var new_point = new BMap.Point(1ng, lat);
        var marker = new BMap.Marker(new_point);  // 创建标注
        map.addOverlay(marker);              // 将标注添加到地图中
        map.panTo(new_point);      
    }
	document.getElementById("theLocation").innerHTML = theLocation();
</script>
</body>
</html>
"""
f.write(message)
f.close()
