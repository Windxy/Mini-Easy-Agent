from brain.Tool import Tool
import requests
from termcolor import cprint
import traceback

class GetWheatherTool(Tool):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
    
    def get_weather_data(self,province, city):
        api_url = f"https://cn.apihz.cn/api/tianqi/tqyb.php?id=88888888&key=88888888&sheng={province}&place={city}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to retrieve data"}
        
    def execute(self, **kwargs):
        try:
            province = self.args.get("province")
            city = self.args.get("city")
            #{'precipitation': 0, 'temperature': 28.1, 'pressure': 1000, 'humidity': 87, 'windDirection': '东南风', 'windDirectionDegree': 178, 'windSpeed': 1.3, 'windScale': '微风', 'code': 200, 'place': '中国, 北京, 北京', 'weather1': '小雨', 'weather2': '中雨'}
            weather_data = self.get_weather_data(province, city)  
            all_weather_data = ''+self.args.get("city")+'天气情况：\n'+weather_data['weather1']+'转'+weather_data['weather2']+'\n'+'温度：'+str(weather_data['temperature'])+'℃\n'+'湿度：'+str(weather_data['humidity'])+'%\n'+'风向：'+weather_data['windDirection']+'\n'+'风速：'+str(weather_data['windSpeed'])+'m/s\n'+'风力：'+weather_data['windScale']+'\n'+'气压：'+str(weather_data['pressure'])+'hPa\n'
            # print(all_weather_data)
            return "工具调用成功"+all_weather_data
        except Exception as e:
            traceback.print_exc()
            return "error:调用get_wheather工具出现错误:" + f"{city}这个城市不存在或无法调用工具查询，我们暂时无法支持，需要提示用户重新输入"

    def before_execution(self, **kwargs):
        super().before_execution(**kwargs)
        
    
    def after_execution(self, response, **kwargs):
        super().after_execution(response, **kwargs)
    
    def pipeline(self, response, **kwargs):
        self.before_execution(**kwargs)
        response = self.execute(**kwargs)
        self.after_execution(response, **kwargs)
        return response