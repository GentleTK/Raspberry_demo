# coding:utf-8
from bottle import template
GEN_HTML = "MarkPoint.html"
def generate(lng, lat):
    template_demo = """
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
    <div id="allmap"></div>
</body>
</html>
<script type="text/javascript">
    // 百度地图API功能
    var map = new BMap.Map("allmap");
	var lng = {{lng}};
	var lat = {{lat}};
    map.centerAndZoom(new BMap.Point(116.331398,39.897445),11);
    map.enableScrollWheelZoom(true);
    
    // 用经纬度设置地图中心点
    function theLocation(){
		map.clearOverlays();
		var new_point = new BMap.Point(lng, lat);
		var marker = new BMap.Marker(new_point);  // 创建标注
		map.addOverlay(marker);              // 将标注添加到地图中
		map.panTo(new_point);      
    }
	document.getElementById("theLocation").innerHTML = theLocation();
</script>
</html>
"""
    html = template(template_demo, lng=lng, lat=lat)
    with open(GEN_HTML, 'wb') as f:
        f.write(html.encode('utf-8'))
def main():
	generate(112.9378, 27.8533)

if __name__ == '__main__':
    main()